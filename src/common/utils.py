from threading import current_thread

class GlobalVariable:
    """Class for adding global variables."""

    def __init__(self):
        """Initialize current thread object."""
        self.thread = current_thread()
        self.attributes_initialized = []

    def set_val(self, attribute, value):
        """Set value."""
        setattr(self.thread, attribute, value)
        self.attributes_initialized.append(attribute)

    def get_val(self, attribute, default=None):
        """Get value."""
        return getattr(self.thread, attribute, default)

    def __enter__(self):
        """Entry function."""
        return self

    def __exit__(self, type, value, traceback):
        """Exit function."""
        for attribute in self.attributes_initialized:
            (delattr(self.thread, attribute) if hasattr(
                self.thread, attribute) else None)


def convert_rupee_to_paisa(rupee):
    """Convert rupee to paisa."""
    return float(rupee * 100)


def convert_paisa_to_rupee(paisa):
    """Convert paisa to rupee."""
    return float(paisa / 100)
