import io
import base64
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv


def encode_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def completion(text, image1):
    if not text:
        return "Please provide some text input."

    _ = load_dotenv(find_dotenv())
    client = OpenAI()

    messages = [{"role": "user", "content": [{"type": "text", "text": text}]}]
    images = [image1]

    for image in images:
        if image is not None:
            base64_image = encode_image_to_base64(image)
            image_message = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            messages[0]["content"].append(image_message)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=1024,
    )

    return response.choices[0].message.content


def main():
    with gr.Blocks(css=".orange-button {background-color: #FF8C00; color: white;}") as gpt4o:
        gr.Markdown("# GPT-4o")

        with gr.Row():
            with gr.Column():
                input_text = gr.Textbox(lines=5, label="Input Text")
            with gr.Column():
                input_images = [gr.Image(type="pil", label=f"Upload Image")]

        submit_button = gr.Button("Run", elem_classes="orange-button")

        output = gr.Textbox(label="Response", interactive=False)

        submit_button.click(fn=completion, inputs=[input_text] + input_images, outputs=output)

        gpt4o.launch()


if __name__ == "__main__":
    main()
