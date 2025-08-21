"""
    ColorDominant: K-Means ile baskın rengi hesaplar ve STRING olarak döndürür.
"""

import os
import sys
import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.Package.src.utils.response import build_response
from components.Package.src.models.PackageModel import PackageModel


class Package(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.color_clusters= self.request.get_param("colorClusters")
        self.max_iterations= self.request.get_param("maxIterations")
        self.target_size= self.request.get_param("targetSize")

        self.image = self.request.get_param("inputImage")


    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def _dominant_color_rgb(self, bgr_img) -> tuple:
        """
        BGR -> RGB, downsample, cv2.kmeans ile (R,G,B) döndür.
        """
        h, w = bgr_img.shape[:2]
        short = min(h, w)
        tsize = max(1, int(self.target_size) if self.target_size else 100)
        scale = max(1, short // tsize)
        ds = bgr_img[::scale, ::scale]

        rgb = cv2.cvtColor(ds, cv2.COLOR_BGR2RGB).reshape(-1, 3).astype(np.float32)

        K = max(1, min(int(self.color_clusters) if self.color_clusters else 4, rgb.shape[0]))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
                    int(self.max_iterations) if self.max_iterations else 100, 1.0)

        _compactness, labels, centers = cv2.kmeans(
            data=rgb, K=K, bestLabels=None, criteria=criteria,
            attempts=1, flags=cv2.KMEANS_PP_CENTERS
        )
        labels = labels.ravel()
        counts = np.bincount(labels, minlength=len(centers))
        dom = centers[int(np.argmax(counts))].round().clip(0, 255).astype(np.uint8)
        return int(dom[0]), int(dom[1]), int(dom[2])  # (R,G,B)

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        r, g, b = self._dominant_color_rgb(img.value)
        self.dominantColor = f"({r}, {g}, {b})"

        packageModel = build_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
