import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

def random_perspective(img, margin=0.2):
	h, w = img.shape[:2]
	# 随机生成四个角点，部分超出原图范围
	pts1 = np.float32([[0,0],[w,0],[w,h],[0,h]]) # type: ignore
	shift = lambda: np.random.uniform(0, margin)
	pts2 = np.float32([
		[-w*shift(), -h*shift()],
		[w*(1+shift()), -h*shift()],
		[w*(1+shift()), h*(1+shift())],
		[-w*shift(), h*(1+shift())]
	]) # type: ignore
	M = cv2.getPerspectiveTransform(pts1, pts2) # type: ignore
	dst = cv2.warpPerspective(img, M, (w, h), borderValue=(0,0,0))
	return dst

def add_natural_glare(img, intensity=0.5):
	"""
	添加自然渐变反光（径向高光+羽化）
	"""
	pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).convert('RGBA')
	w, h = pil_img.size
	overlay = Image.new('RGBA', pil_img.size, (255,255,255,0))
	for _ in range(np.random.randint(1,3)):
		# 反光中心、半径、透明度
		cx, cy = np.random.randint(w//4, w*3//4), np.random.randint(h//8, h*7//8)
		rx, ry = np.random.randint(w//4, w//3), np.random.randint(h//4, h//3)
		alpha = int(255 * intensity * np.random.uniform(0.15, 0.35))
		# 画白色椭圆
		glare = Image.new('L', pil_img.size, 0)
		draw = ImageDraw.Draw(glare)
		draw.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], fill=alpha)
		# 羽化（高斯模糊）
		glare = glare.filter(ImageFilter.GaussianBlur(radius=w//5))
		# 合成到overlay
		overlay = ImageChops.add(overlay, Image.merge('RGBA', [glare]*3 + [glare]))
	out = Image.alpha_composite(pil_img, overlay)
	return cv2.cvtColor(np.array(out.convert('RGB')), cv2.COLOR_RGB2BGR)

def add_blur(img, ksize=11):
	pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).convert('RGBA')
	w, h = pil_img.size
	ksize = min(w//50*2+1, h//50*2+1)  # 保证ksize不超过图像尺寸且为奇数
	return cv2.GaussianBlur(img, (ksize, ksize), 0)

def add_moire(img, strength=0.2):
	h, w = img.shape[:2]
	freq = np.random.uniform(0.1, 0.3)
	angle = np.random.uniform(0, np.pi)
	phase = np.random.uniform(0, np.pi)
	yy, xx = np.meshgrid(np.arange(h), np.arange(w), indexing='ij')
	pattern = np.sin(freq * (xx * np.cos(angle) + yy * np.sin(angle)) + phase)
	# 生成从左到右的渐变mask，左0右1
	mask = np.linspace(0, 1, w)[None, :]
	# strength在左侧为0，右侧为原strength
	local_strength = strength * mask
	moire = ((pattern + 1) / 2 * 255 * local_strength).astype(np.uint8)
	moire = cv2.merge([moire]*3)
	img = cv2.addWeighted(img, 1, moire, 0.5, 0)
	return img


def process(path: str):
	img = cv2.imread(path)
	img = add_natural_glare(img, 5)
	img = random_perspective(img, 0.4)
	img = add_blur(img, ksize=np.random.choice([15, 21, 27]))
	img = add_moire(img)
	cv2.imwrite(path, img)

if __name__ == "__main__":
	process("/home/lee/project/qBot/nb/disablePlugins/tohoschedule/ad.webp", "output.jpg")