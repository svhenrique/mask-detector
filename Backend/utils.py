from PySide6.QtGui import QImage
import numpy as np

def toQImage(image):
    """
        Entrada: objeto numpy padrão retornado por imread do opencv-python,
        ou seja, utilizando 3 canais de cores em formato BGR
    """
    assert (np.max(image) <= 255)
    image8 = image.astype(np.uint8, order='C', casting='unsafe')
    height = image8.shape[0]
    width = image8.shape[1]
    bytes_per_line = 3 * width
    qimage = QImage(image8.data, width, height, bytes_per_line,
                    QImage.Format_BGR888)
    return qimage