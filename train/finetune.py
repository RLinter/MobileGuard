# Load libraries
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training, PeftModel
from datasets import Dataset
import torch
import json
def tokenize_function(example):
    # Concatenate prompt + completion
    full_text = example["prompt"] + example["completion"]

    # Tokenize the full sequence
    tokenized = tokenizer(full_text, truncation=True, padding="max_length", max_length=2048)

    # Create label mask: mask out the prompt tokens
    prompt_ids = tokenizer(example["prompt"], truncation=True, max_length=2048)["input_ids"]
    labels = tokenized["input_ids"].copy()
    labels[:len(prompt_ids)] = [-100] * len(prompt_ids)  # ignore prompt during loss

    tokenized["labels"] = labels
    return tokenized

def load_finetuned_model(model_name):
    base_model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.float16,
        token=True,
    )

    # Load your fine-tuned LoRA
    model = PeftModel.from_pretrained(base_model, "./llama3-unsafe-instruct/checkpoint-20/")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer

# main function
if __name__ == "__main__":
    model_name = "BlitherBoom/AutoDroid-V2"

    # Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True, token=True)
    tokenizer.pad_token = tokenizer.eos_token

    # Model
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.float16,
        token=True,
    )
    model.config.pad_token_id = tokenizer.pad_token_id

    model = prepare_model_for_kbit_training(model)

    # Apply LoRA
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )

    model = get_peft_model(model, lora_config)

    with open("formatted_data.jsonl", "r") as f:
        data = [json.loads(line) for line in f]

    # Convert list of dicts to Hugging Face Dataset
    dataset = Dataset.from_list(data)
    tokenized_dataset = dataset.map(tokenize_function, batched=False)

    training_args = TrainingArguments(
        output_dir="./llama3-unsafe-instruct",
        per_device_train_batch_size=1,      
        gradient_accumulation_steps=8,        
        num_train_epochs=10,
        learning_rate=2e-4,
        fp16=True,
        save_strategy="epoch",
        logging_steps=10,
        save_total_limit=2,
    )

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator,
    )

    trainer.train()