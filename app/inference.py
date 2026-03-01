import torch
import torch.nn.functional as F
import model_loader 

@torch.no_grad()
def extract_audio_embedding_voxtral(model, inputs):
    audio_outputs = model.audio_tower(input_features=inputs["input_features"])
    audio_hidden = audio_outputs.last_hidden_state
    embedding = audio_hidden.mean(dim=1)
    return F.normalize(embedding, p=2, dim=1)

@torch.no_grad()
def extract_audio_embedding_wavlm(model, inputs):
    audio_outputs = model(**inputs)
    audio_hidden = audio_outputs.last_hidden_state
    embedding = audio_hidden.mean(dim=1)
    return F.normalize(embedding, p=2, dim=1)

@torch.no_grad()
def generate_merged_embedding(waveform, sampling_rate):
    waveform_np = waveform.squeeze().cpu().numpy()

    # Voxtral inputs
    inputs_voxtral = model_loader.feat_extractor_1(
        waveform_np,
        sampling_rate=sampling_rate,
        return_tensors="pt"
    )
    inputs_voxtral = {k: v.to(model_loader.model_1.device) for k, v in inputs_voxtral.items()}
    inputs_voxtral["input_features"] = inputs_voxtral["input_features"].to(torch.bfloat16)

    emb_vox = extract_audio_embedding_voxtral(model_loader.model_1, inputs_voxtral)

    # WavLM inputs
    # WavLM expects numpy array [time,], flatten if necessary
    inputs_wavlm = model_loader.feature_extractor_2(
        waveform_np,
        sampling_rate=sampling_rate,
        return_tensors="pt"
    )
    inputs_wavlm = {k: v.to(model_loader.model_2.device) for k, v in inputs_wavlm.items()}
    emb_wavlm = extract_audio_embedding_wavlm(model_loader.model_2, inputs_wavlm)

    # Merge embeddings
    merged_embedding = torch.cat([emb_vox, emb_wavlm], dim=1)

    return merged_embedding
