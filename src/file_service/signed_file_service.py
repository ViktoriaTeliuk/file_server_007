import file_service


class SignedFileService(file_service.FileService):

    def __init__(self, wrapped_file_service: file_service.FileService):
        self.wrapped_file_service = wrapped_file_service

    def read(self, filename: str) -> str:
        data = read_file(filename)
        for label in SignatureFactory.signers:
            sig_filename = f"{filename}.{label}"
            if check_file(sig_filename):
                signer = SignatureFactory.get_signer(label)
                actual_sig = signer(data)
                expected_sig = read_file(sig_filename)

                if actual_sig == expected_sig:
                    return data
                else:
                    raise Exception("File is broken")

    def write(self, filename: str) -> str:
        filename = create_file(content)
        sig_filename = f"{filename}.{label}"
        with open(sig_filename, "w") as f:
            signer = SignatureFactory.get_signer(label)
            f.write(signer(content))
        return filename, sig_filename

    def remove(self, filename: str): return None

    def ls(self) -> [str]: return ()

    def cd(self, dirname: str) -> None:
        pass

    async def async_write(self, content: str) -> str:
        return self.write(content.encode())

