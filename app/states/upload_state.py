import reflex as rx
import random
import string


class UploadState(rx.State):
    uploaded_files: list[str] = []
    labels: dict[str, str] = {}
    is_uploading: bool = False

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the file upload."""
        if not files:
            yield rx.toast.error("No files selected")
            return
        self.is_uploading = True
        yield
        upload_dir = rx.get_upload_dir()
        upload_dir.mkdir(parents=True, exist_ok=True)
        new_files = []
        for file in files:
            data = await file.read()
            unique_id = "".join(
                random.choices(string.ascii_letters + string.digits, k=8)
            )
            filename = f"{unique_id}_{file.name}"
            file_path = upload_dir / filename
            with file_path.open("wb") as f:
                f.write(data)
            new_files.append(filename)
            self.labels[filename] = ""
        self.uploaded_files.extend(new_files)
        self.is_uploading = False
        yield rx.toast.success(f"Uploaded {len(files)} sample(s)")

    @rx.event
    def update_label(self, filename: str, value: str):
        """Update the character label for a specific file."""
        self.labels[filename] = value

    @rx.event
    def remove_file(self, filename: str):
        """Remove a file from the list (UI only for now, keeping file on disk is safer)."""
        if filename in self.uploaded_files:
            self.uploaded_files.remove(filename)
        if filename in self.labels:
            del self.labels[filename]

    @rx.var
    def file_count(self) -> int:
        return len(self.uploaded_files)

    @rx.var
    def has_files(self) -> bool:
        return len(self.uploaded_files) > 0