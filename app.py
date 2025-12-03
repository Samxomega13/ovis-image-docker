import os
import time
import threading
import torch
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file
import gradio as gr
from ovis_image.model.tokenizer import build_ovis_tokenizer
from ovis_image.model.autoencoder import load_ae
from ovis_image.model.hf_embedder import OvisEmbedder
from ovis_image.model.model import OvisImageModel
from ovis_image.sampling import generate_image, save_image
from ovis_image import ovis_image_configs

app = FastAPI(title="Ovis-Image API", version="1.0")

class GenerateRequest(BaseModel):
    prompt: str
    negative_prompt: str = ""
    image_size: int = 1024
    denoising_steps: int = 50
    cfg_scale: float = 5.0
    seed: int = 42

class ModelManager:
    def __init__(self):
        self.model = None
        self.autoencoder = None
        self.ovis_encoder = None
        self.ovis_tokenizer = None
        self.device = "cuda"
        self.dtype = torch.bfloat16
        self.last_used = 0
        self.idle_timeout = int(os.getenv("IDLE_TIMEOUT", "300"))
        self.lock = threading.Lock()
        threading.Thread(target=self._idle_checker, daemon=True).start()

    def _download_model(self, path_or_repo):
        """Download model from HuggingFace if needed"""
        if os.path.exists(path_or_repo):
            return path_or_repo
        
        # Parse HuggingFace repo format: AIDC-AI/Ovis-Image-7B/ovis_image.safetensors
        parts = path_or_repo.split('/')
        if len(parts) >= 3:
            repo_id = f"{parts[0]}/{parts[1]}"
            filename = '/'.join(parts[2:])
            print(f"Downloading {filename} from {repo_id}...")
            return hf_hub_download(repo_id=repo_id, filename=filename)
        return path_or_repo

    def load_models(self):
        with self.lock:
            if self.model is not None:
                self.last_used = time.time()
                return
            
            model_path = self._download_model(os.getenv("MODEL_PATH", "AIDC-AI/Ovis-Image-7B/ovis_image.safetensors"))
            vae_path = self._download_model(os.getenv("VAE_PATH", "AIDC-AI/Ovis-Image-7B/ae.safetensors"))
            ovis_path = os.getenv("OVIS_PATH", "AIDC-AI/Ovis2.5-2B")
            
            model_config = ovis_image_configs["ovis-image-7b"]
            self.model = OvisImageModel(model_config)
            model_state_dict = load_file(model_path)
            self.model.load_state_dict(model_state_dict)
            self.model = self.model.to(device=self.device, dtype=self.dtype)
            self.model.eval()
            
            self.ovis_tokenizer = build_ovis_tokenizer(ovis_path)
            self.autoencoder = load_ae(vae_path, model_config.autoencoder_params, 
                                      device=self.device, dtype=self.dtype, random_init=False)
            self.autoencoder.eval()
            self.ovis_encoder = OvisEmbedder(model_path=ovis_path, random_init=False,
                                            low_cpu_mem_usage=True, torch_dtype=torch.bfloat16)
            self.ovis_encoder = self.ovis_encoder.to(device=self.device, dtype=self.dtype)
            
            self.last_used = time.time()

    def unload_models(self):
        with self.lock:
            if self.model is not None:
                del self.model, self.autoencoder, self.ovis_encoder, self.ovis_tokenizer
                self.model = None
                torch.cuda.empty_cache()

    def _idle_checker(self):
        while True:
            time.sleep(60)
            if self.model and time.time() - self.last_used > self.idle_timeout:
                self.unload_models()

    def generate(self, prompt, image_size, denoising_steps, cfg_scale, seed):
        self.load_models()
        with torch.no_grad():
            image = generate_image(
                device=self.device, dtype=self.dtype, model=self.model,
                prompt=prompt, autoencoder=self.autoencoder,
                ovis_tokenizer=self.ovis_tokenizer, ovis_encoder=self.ovis_encoder,
                img_height=image_size, img_width=image_size,
                denoising_steps=denoising_steps, cfg_scale=cfg_scale, seed=seed
            )
        self.last_used = time.time()
        return image

manager = ModelManager()

@app.post("/api/generate")
async def api_generate(req: GenerateRequest):
    try:
        image = manager.generate(req.prompt, req.image_size, req.denoising_steps, req.cfg_scale, req.seed)
        filename = f"output_{int(time.time())}.png"
        save_image(filename, "outputs", image, True, req.prompt, False)
        return {"status": "success", "image": f"/outputs/{filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/outputs/{filename}")
async def get_image(filename: str):
    path = f"outputs/{filename}"
    if os.path.exists(path):
        return FileResponse(path)
    raise HTTPException(status_code=404, detail="Image not found")

def gradio_generate(prompt, image_size, steps, cfg, seed, timeout):
    manager.idle_timeout = timeout * 60
    image = manager.generate(prompt, image_size, steps, cfg, seed)
    filename = f"output_{int(time.time())}.png"
    save_image(filename, "outputs", image, True, prompt, False)
    return f"outputs/{filename}"

with gr.Blocks(title="Ovis-Image") as demo:
    gr.Markdown("# 🎨 Ovis-Image Text-to-Image Generator")
    
    with gr.Tabs():
        with gr.Tab("🖼️ Generate | 生成"):
            with gr.Row():
                with gr.Column():
                    prompt = gr.Textbox(label="Prompt | 提示词", lines=3, 
                                       placeholder="Describe the image you want to generate...")
                    with gr.Accordion("⚙️ Advanced Settings | 高级设置", open=False):
                        size = gr.Slider(512, 2048, 1024, step=64, label="Image Size | 图像尺寸")
                        steps = gr.Slider(20, 100, 50, step=1, label="Denoising Steps | 去噪步数")
                        cfg = gr.Slider(1.0, 15.0, 5.0, step=0.5, label="CFG Scale | 引导比例")
                        seed = gr.Number(42, label="Seed | 随机种子")
                        timeout = gr.Slider(1, 60, 5, step=1, label="Idle Timeout (min) | 空闲超时(分钟)")
                    btn = gr.Button("🚀 Generate | 生成", variant="primary")
                with gr.Column():
                    output = gr.Image(label="Generated Image | 生成的图像")
            
            btn.click(gradio_generate, [prompt, size, steps, cfg, seed, timeout], output)
        
        with gr.Tab("📖 API Docs | API文档"):
            gr.Markdown("""
            ## REST API Endpoints
            
            ### POST /api/generate
            ```json
            {
              "prompt": "your prompt here",
              "image_size": 1024,
              "denoising_steps": 50,
              "cfg_scale": 5.0,
              "seed": 42
            }
            ```
            
            ### GET /outputs/{filename}
            Download generated images
            
            ### Swagger UI
            Visit `/docs` for interactive API documentation
            """)

app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "7860"))
    uvicorn.run(app, host="0.0.0.0", port=port)
