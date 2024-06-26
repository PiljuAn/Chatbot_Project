import torch
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast
import logging

logger = logging.getLogger(__name__)


Q_TKN = "<usr>" # 사용자 질문 토큰
A_TKN = "<sys>" # 시스템 응답 토큰
BOS = '</s>' # 시작 토큰
EOS = '</s>' # 종료 토큰
MASK = '<unused0>' # 마스크 토큰 (답변을 가릴 때 사용)
SENT = '<unused1>' # 문장 구분 토큰
PAD = '<pad>' # 패딩 토큰 (시퀀스의 길이를 맞추기 위해 사용)

gpt2_model = None
koGPT2_TOKENIZER = None

def load_model():
    global gpt2_model, koGPT2_TOKENIZER
    
    if koGPT2_TOKENIZER is None:
        logger.info('chatting_model.py/load_model -> koGPT2_TOKENIZER is loaded')
        koGPT2_TOKENIZER = PreTrainedTokenizerFast.from_pretrained(
            "skt/kogpt2-base-v2", # KoGPT2 모델의 사전 학습된 가중치를 불러옴
            bos_token=BOS, 
            eos_token=EOS, 
            unk_token='<unk>', # 알 수 없는 토큰 설정
            pad_token=PAD, 
            mask_token=MASK
            )
    else:
        logger.info('chatting_model.py/load_model -> Use cached koGPT2_TOKENIZER')

    if gpt2_model is None:
        logger.info('chatting_model.py/load_model -> gpt2 model is loaded')
        model_path = "/app/chatbot/service_model/kogpt2_chatbot_model.pth"
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        gpt2_model = GPT2LMHeadModel.from_pretrained('skt/kogpt2-base-v2')
        gpt2_model.load_state_dict(torch.load(model_path, map_location=device)['model_state_dict'])
        gpt2_model.eval()
        gpt2_model.to(device)
    else:
        logger.info('chatting_model.py/load_model -> Use cached gpt2 model')

def chatting_model(user_input, model_path):
    global gpt2_model, koGPT2_TOKENIZER
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    load_model()

    response = ""

    ### 그라디언트 계산 비활성화(추론 단계에서 필요 없음) ###
    with torch.no_grad():   
        q = user_input.strip()
        a = ""
        while True:
            ### 입력 토큰화 및 텐서 변환 ##
            input_ids = torch.LongTensor(koGPT2_TOKENIZER.encode(Q_TKN + q + SENT + A_TKN + a)).unsqueeze(dim=0).to(device)
            
        #################################################### 모델 예측 수행 ####################################################
            outputs = gpt2_model(input_ids)
            logits = outputs.logits
            logits = logits[:, -1, :]  
            probs = logits.softmax(dim=-1) 
            top_prob, top_idx = torch.topk(probs, k=1, dim=-1) 
            gen_token_id = top_idx.item()
            gen = koGPT2_TOKENIZER.convert_ids_to_tokens(gen_token_id) 
            if gen == EOS: 
                break
            a += gen.replace("▁", " ")
            
        response = a.strip()

    return response