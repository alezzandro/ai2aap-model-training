#!/opt/app-root/bin/python

from huggingface_hub import login
login(token="***", write_permission=True)

from datasets import load_dataset
tickets_train = load_dataset("csv", data_files={"train": "900tickets-300WS-300DB-300FS-train.csv"}, split='train')
tickets_test = load_dataset("csv", data_files={"test": "900tickets-300WS-300DB-300FS-test.csv"}, split='test')

tickets_train.to_json("itsm_tickets-train.jsonl")
tickets_test.to_json("itsm_tickets-test.jsonl")

from huggingface_hub import Repository

repo_url = "https://huggingface.co/datasets/alezzandro/itsm_tickets"
repo = Repository(local_dir="../itsm_tickets", clone_from=repo_url)
#!cp issues-datasets-with-comments.jsonl github-issues/