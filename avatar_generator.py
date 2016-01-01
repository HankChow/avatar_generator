import Image
import ImageDraw
import random
import md5
import sys
import time
import os

class avatar_generator:
	
	def str2meta(self, string):
		md5str = md5.md5(string).hexdigest()
		color1 = eval('0x' + md5str[-6:])
		color2 = eval('0x' + md5str[-12:-6])
		color3 = eval('0x' + md5str[-18:-12])
		darkest = min(color1, color2, color3)
		lightest = max(color1, color2, color3)
		foreground = 0
		background = 0
		if eval('0x' + md5str[-19]) % 2 == 0:
			foreground = darkest
			background = lightest
		else:
			foreground = lightest
			background = darkest
		symmetry_method = ''
		if eval('0x' + md5str[-20]) % 4 == 0:
			symmetry_method = 'x_axial_symmetry'
		elif eval('0x' + md5str[12]) % 4 == 1:
			symmetry_method = 'semi_centrosymmetry'
		elif eval('0x' + md5str[12]) % 4 == 2:
			symmetry_method = 'quad_centrosymmetry'
		else:
			symmetry_method = 'counter_quad_centrosymmetry'
		avatarDetails = []
		md5_block = []
		for i in range(0, 4):
			md5_block.append(md5str[(i * 3):((i + 1) * 3)])
		if symmetry_method == 'quad_centrosymmetry' or symmetry_method == 'counter_quad_centrosymmetry':
			for i in range(0, 4):
				avatarDetails.append(str(bin(eval('0x' + md5_block[i][1])))[2:].zfill(4))
		else:
			for i in range(0, 4):
				avatarDetails.append(str(bin(eval('0x' + md5_block[i][0])))[2:].zfill(4))
				avatarDetails.append(str(bin(eval('0x' + md5_block[i][2])))[2:].zfill(4))
		avatarInfo = {
		'avatarDetails' : avatarDetails, 
		'symmetry_method' : symmetry_method, 
		'foreground' : foreground, 
		'background' : background
		}
		return avatarInfo
		
	def meta_generator(self, avatarInfo, x_len = 400, y_len = 400, block_len = 50):
		meta = ''
		if avatarInfo['symmetry_method'] == 'quad_centrosymmetry' or avatarInfo['symmetry_method'] == 'counter_quad_centrosymmetry':
			meta = Image.new('RGB', (x_len / 2, y_len / 2))
			blocks = ImageDraw.Draw(meta)
			x_count = 0
			y_count = 0
			for x in range(0, x_len / 2, block_len):
				for y in range(0, y_len / 2, block_len):
					blocks_poly = [(x, y), (x + block_len, y), (x + block_len, y + block_len), (x, y + block_len)]
					if avatarInfo['avatarDetails'][x_count][y_count] == '0':
						blocks.polygon(blocks_poly, fill = avatarInfo['background'])
					else:
						blocks.polygon(blocks_poly, fill = avatarInfo['foreground'])
					y_count += 1
				y_count = 0
				x_count += 1
			return {'meta' : meta, 'sym_info' : avatarInfo['symmetry_method']}
		else:
			meta = Image.new('RGB', (x_len, y_len / 2))
			blocks = ImageDraw.Draw(meta)
			x_count = 0
			y_count = 0
			for x in range(0, x_len, block_len):
				for y in range(0, y_len / 2, block_len):
					blocks_poly = [(x, y), (x + block_len, y), (x + block_len, y + block_len), (x, y + block_len)]
					if avatarInfo['avatarDetails'][x_count][y_count] == '0':
						blocks.polygon(blocks_poly, fill = avatarInfo['background'])
					else:
						blocks.polygon(blocks_poly, fill = avatarInfo['foreground'])
					y_count += 1
				y_count = 0
				x_count += 1
			return {'meta' : meta, 'sym_info' : avatarInfo['symmetry_method']}

	def random_meta_generator(self, x_len = 200, y_len = 200, block_len = 50):
		meta = Image.new('RGB', (x_len, y_len))
		blocks = ImageDraw.Draw(meta)
		for x in range(0, x_len + block_len, block_len):
			for y in range(0, y_len + block_len, block_len):
				blocks_poly = [(x, y), (x + block_len, y), (x + block_len, y + block_len), (x, y + block_len)]
				randR = random.randint(0, 256)
				randG = random.randint(0, 256)
				randB = random.randint(0, 256)
				color = randR * 65536 + randG * 4096 + randB
				blocks_fill = blocks.polygon(blocks_poly, fill = color)
		return {'meta' : meta, 'sym_info' : 'quad_centrosymmetry'}

	def avatar_generator(self, meta):
		avatar = ''
		if meta['sym_info'] == 'x_axial_symmetry':
			avatar = self.x_axial_symmetry(meta['meta'])
		elif meta['sym_info'] == 'counter_quad_centrosymmetry':
			avatar = self.counter_quad_centrosymmetry(meta['meta'])
		elif meta['sym_info'] == 'semi_centrosymmetry':
			avatar = self.semi_centrosymmetry(meta['meta'])
		else:
			avatar = self.quad_centrosymmetry(meta['meta'])
		return avatar
	
	def x_axial_symmetry(self, meta):
		avatar = Image.new('RGB', (meta.size[0], meta.size[1] * 2))
		avatar.paste(meta, (0, 0))
		trans = meta.transpose(Image.FLIP_TOP_BOTTOM)
		avatar.paste(trans, (0, meta.size[1]))
		return avatar
	
	def y_axial_symmetry(self, meta):
		avatar = Image.new('RGB', (meta.size[0] * 2, meta.size[1]))
		avatar.paste(meta, (0, 0))
		trans = meta.transpose(Image.FLIP_LEFT_RIGHT)
		avatar.paste(trans, (meta.size[0], 0))
		return avatar
	
	def semi_centrosymmetry(self, meta):
		avatar = Image.new('RGB', (meta.size[0], meta.size[1] * 2))
		avatar.paste(meta, (0, 0))
		avatar.paste(meta.rotate(180), (0, meta.size[1]))
		return avatar
	
	def quad_centrosymmetry(self, meta):
		avatar = Image.new('RGB', (meta.size[0] * 2, meta.size[1] * 2))
		avatar.paste(meta, (0, 0))
		avatar.paste(meta.rotate(90), (0, meta.size[1]))
		avatar.paste(meta.rotate(180), (meta.size[0], meta.size[1]))
		avatar.paste(meta.rotate(270), (meta.size[0], 0))
		return avatar
	
	def counter_quad_centrosymmetry(self, meta):
		avatar = Image.new('RGB', (meta.size[0] * 2, meta.size[1] * 2))
		avatar.paste(meta, (0, 0))
		avatar.paste(meta.rotate(270), (0, meta.size[1]))
		avatar.paste(meta.rotate(180), (meta.size[0], meta.size[1]))
		avatar.paste(meta.rotate(90), (meta.size[0], 0))
		return avatar
		
if __name__ == '__main__':
	if len(sys.argv) != 2:
		sys.argv.append(str(time.time()))
	ag = avatar_generator()
	meta = ag.meta_generator(ag.str2meta(sys.argv[1]))
	avatar = ag.avatar_generator(meta)
	avatar.show()
	if not os.path.exists('history/'):
		os.makedirs('history/')
	if not os.path.exists('history/' + sys.argv[1] + '.jpg'):
		avatar.save('history/' + sys.argv[1] + '.jpg', 'JPEG')
