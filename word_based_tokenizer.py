import re

class SimpleWordBasedTokenizer:
    def __init__(self, split_regex:str=r'([,.:;?_!"\'()]|--|\s)', sub_regex:str=r'\s+([,.?!"()\'])'):
        # token -> token id
        self.token_to_toke_id = {}
        self.split_regex = split_regex
        self.sub_regex = sub_regex
        
    def create_vocabs(self, raw_text):
        """Create vocabulary on raw text dataset"""
        preprocessed = re.split(self.split_regex, raw_text)
        # strip all whitespaces tokens
        preprocessed = [item.strip() for item in preprocessed if item.strip()]
        
        # add special tokens
        all_tokens = sorted(set(preprocessed))
        all_tokens.extend(['<|endoftext|>', '<|unk|>'])
        
        self.token_to_toke_id = {token: token_id for token_id, token in enumerate(all_tokens)} # vocabs
        
        self.token_id_to_token = {i:s for s,i in self.token_to_toke_id.items()}
        
        return self.token_to_toke_id
        
    def get_vocab(self):
        return self.token_to_toke_id
        
    def encode(self, text):
        
        preprocessed = re.split(self.split_regex, text)
        # strip all whitespaces tokens
        preprocessed = [item.strip() for item in preprocessed if item.strip()]
        preprocessed = [
            item if item in self.token_to_toke_id else "<|unk|>" for item in preprocessed
        ]
        
        # accessing a value by its key in the dictory, that is all what this line is does
        # sees 'A' it looks for the a key of 'A' and return it corresponding value which is the token id
        ids = [self.token_to_toke_id[s] for s in preprocessed]
        return ids
    
    def decode(self, ids):
        # similar concept in the encoder... looks for key from the decoder dict, which here is the token id, finding the token key, gives the token itself, that is the word in search
        text = " ".join([self.token_id_to_token[i] for i in ids])
        # replace spaces before the specified punctuations
        # eg of what this line does, eg: John is a boy . -> John is a boy.
        text = re.sub(self.sub_regex, r'\1', text)
        return text