class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class MqttError(AppException):
    """Raised for MQTT-related errors"""
    pass

class NotFoundError(AppException):
    """Raised when a resource is not found."""
    pass


class ValidationError(AppException):
    """Raised for data validation errors."""
    pass
