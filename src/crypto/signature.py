import hashlib


class SignatureFactory(type):
    signers = {}

    def __new__(cls, classname, parents, attributes):
        if "__call__" not in attributes:
            raise Exception(f"Signer class must implement __call_ function : {classname}")
        # label = attributes["label"] if "label" in attributes else classname.lower()
        signer_class = type(classname, parents, attributes)
        if "label" not in attributes:
            signer_class.label = classname.lower()
        SignatureFactory.signers[signer_class.label] = signer_class()

        def signature_filename(self, filename):
            return f"{filename}.{signer_class.label}"

        return signer_class

    @staticmethod
    def get_signer(label: str):
        return SignatureFactory.signers[label]


class MD5Signer(metaclass=SignatureFactory):
    label = "md5"

    def __call__(self, data: str) -> str:
        return hashlib.md5(data.encode()).hexdigest()


class Sha512Signer(metaclass=SignatureFactory):
    def __call__(self, data: str) -> str:
        return hashlib.sha512(data.encode()).hexdigest()
