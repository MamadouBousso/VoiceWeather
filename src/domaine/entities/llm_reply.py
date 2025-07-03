class LLMReply:
    def __init__(self, texte, source="", audio_path=None):
        self.texte = texte
        self.source = source
        self.audio_path = audio_path 