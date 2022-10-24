import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
import io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

use_auth_token = "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"

pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    revision="fp16",
    torch_dtype=torch.float16,
    use_auth_token=use_auth_token)
pipe = pipe.to("cuda")


def stablediffusion(prompt):
    with autocast("cuda"):
            image = pipe(
                prompt=prompt,           # 入力テキスト
                height=512,              # 出力画像の高さ
                width=512,               # 出力画像の幅
                num_inference_steps=50,  # 画像生成に費やすステップ数
                guidance_scale=7.5,      # プロンプトと出力画像の類似度
                generator=None           # 乱数シードジェネレータ
                )["sample"][0]

    image.save("./images/generate.png")