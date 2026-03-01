import torch
from transformers import (
    VoxtralRealtimeProcessor,
    VoxtralRealtimeForConditionalGeneration,
    AutoFeatureExtractor,
    AutoModel
)

device = "cuda" if torch.cuda.is_available() else "cpu"

# Global variables
model_1 = None
feat_extractor_1 = None
model_2 = None
feature_extractor_2 = None

def load_models():
    global model_1, feat_extractor_1
    global model_2, feature_extractor_2

    # -------- Voxtral --------
    model_id_1 = "mistralai/Voxtral-Mini-4B-Realtime-2602"

    feat_extractor_1 = VoxtralRealtimeProcessor.from_pretrained(model_id_1)

    model_1 = VoxtralRealtimeForConditionalGeneration.from_pretrained(
        model_id_1,
        torch_dtype=torch.bfloat16,
        device_map=device
    )

    model_1.to(device)
    model_1.eval()

    # -------- WavLM --------
    model_id_2 = "microsoft/wavlm-base-plus-sv"

    feature_extractor_2 = AutoFeatureExtractor.from_pretrained(model_id_2)

    model_2 = AutoModel.from_pretrained(
        model_id_2
    ).to(device)

    model_2.eval()

    print("✅ Models loaded successfully") 
