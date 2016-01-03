import Image, ImageDraw
import sys, os
import random
import hashlib
import time
import math
import ConfigParser

class avatar_generator:
	
	
	def str2meta_md5(self, string):

		md5str = hashlib.md5(string).hexdigest()

		color1 = eval('0x' + md5str[-6:])
		color2 = eval('0x' + md5str[-12:-6])
		color3 = eval('0x' + md5str[-18:-12])
		darkest = 0
		lightest = 0
		distance1 = self.cal_distance(color2, color3)
		distance2 = self.cal_distance(color1, color3)
		distance3 = self.cal_distance(color1, color2)
		if max(distance1, distance2, distance3) == distance1:
			darkest = min(color2, color3)
			lightest = max(color2, color3)
		elif max(distance1, distance2, distance3) == distance2:
			darkest = min(color1, color3)
			lightest = max(color1, color3)
		else:
			darkest = min(color1, color2)
			lightest = max(color1, color2)
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
		elif eval('0x' + md5str[-20]) % 4 == 1:
			symmetry_method = 'semi_centrosymmetry'
		elif eval('0x' + md5str[-20]) % 4 == 2:
			symmetry_method = 'quad_centrosymmetry'
		else:
			symmetry_method = 'counter_quad_centrosymmetry'
		
		metaDetails = []
		md5_block = []
		for i in range(0, 4):
			md5_block.append(md5str[(i * 3):((i + 1) * 3)])
		if symmetry_method == 'quad_centrosymmetry' or symmetry_method == 'counter_quad_centrosymmetry':
			for i in range(0, 4):
				metaDetails.append(str(bin(eval('0x' + md5_block[i][1])))[2:].zfill(4))
		else:
			for i in range(0, 4):
				metaDetails.append(str(bin(eval('0x' + md5_block[i][0])))[2:].zfill(4))
				metaDetails.append(str(bin(eval('0x' + md5_block[i][2])))[2:].zfill(4))
		
		metaInfo = {
		'metaDetails' : metaDetails, 
		'symmetry_method' : symmetry_method, 
		'foreground' : foreground, 
		'background' : background, 
		'hash' : 'md5'
		}
		
		return metaInfo
	
	
	def str2meta_sha256(self, string):
		
		sha256str = hashlib.sha256(string).hexdigest()
		
		color1 = eval('0x' + sha256str[-6:])
		color2 = eval('0x' + sha256str[-12:-6])
		color3 = eval('0x' + sha256str[-18:-12])
		darkest = 0
		lightest = 0
		distance1 = self.cal_distance(color2, color3)
		distance2 = self.cal_distance(color1, color3)
		distance3 = self.cal_distance(color1, color2)
		if max(distance1, distance2, distance3) == distance1:
			darkest = min(color2, color3)
			lightest = max(color2, color3)
		elif max(distance1, distance2, distance3) == distance2:
			darkest = min(color1, color3)
			lightest = max(color1, color3)
		else:
			darkest = min(color1, color2)
			lightest = max(color1, color2)
		foreground = 0
		background = 0
		if eval('0x' + sha256str[-19]) % 2 == 0:
			foreground = darkest
			background = lightest
		else:
			foreground = lightest
			background = darkest
		
		symmetry_dic = {
		'0' : 'non_nesting_x_axial_symmetry', 
		'1' : 'non_nesting_semi_centrosymmetry',
		'2' : 'non_nesting_quad_centrosymmetry',
		'3' : 'non_nesting_counter_quad_centrosymmetry',
		'4' : 'quad_centrosymmetry_nesting_x_axial_symmetry',
		'5' : 'quad_centrosymmetry_nesting_semi_centrosymmetry',
		'6' : 'quad_centrosymmetry_nesting_quad_centrosymmetry',
		'7' : 'quad_centrosymmetry_nesting_counter_quad_centrosymmetry',
		'8' : 'counter_quad_centrosymmetry_nesting_x_axial_symmetry',
		'9' : 'counter_quad_centrosymmetry_nesting_semi_centrosymmetry',
		'a' : 'counter_quad_centrosymmetry_nesting_quad_centrosymmetry',
		'b' : 'counter_quad_centrosymmetry_nesting_counter_quad_centrosymmetry',
		'c' : 'x_axial_symmetry_nesting_x_axial_symmetry',
		'd' : 'x_axial_symmetry_nesting_semi_centrosymmetry',
		'e' : 'semi_centrosymmetry_nesting_x_axial_symmetry',
		'f' : 'semi_centrosymmetry_nesting_semi_centrosymmtry'
		}
		symmetry_method = symmetry_dic[sha256str[-20]]
		
		metaDetails = []
		sha256_block = []
		for i in range(0, 16):
			sha256_block.append(sha256str[(i * 3):((i + 1) * 3)])
		if symmetry_method in ['non_nesting_quad_centrosymmetry', 'non_nesting_counter_quad_centrosymmetry']:
			for i in range(0, 8):
				metaDetails.append(str(bin(eval('0x' + sha256_block[i][1])))[2:].zfill(4) + str(bin(eval('0x' + sha256_block[i + 8][1])))[2:].zfill(4))
		elif symmetry_method in ['non_nesting_x_axial_symmetry', 'non_nesting_semi_centrosymmetry']:
			for i in range(0, 8):
				metaDetails.append(str(bin(eval('0x' + sha256_block[i][0])))[2:].zfill(4) + str(bin(eval('0x' + sha256_block[i + 8][0])))[2:].zfill(4))
				metaDetails.append(str(bin(eval('0x' + sha256_block[i][2])))[2:].zfill(4) + str(bin(eval('0x' + sha256_block[i + 8][2])))[2:].zfill(4))
		elif symmetry_method in ['quad_centrosymmetry_nesting_x_axial_symmetry', 'quad_centrosymmetry_nesting_semi_centrosymmetry', 'counter_quad_centrosymmetry_nesting_x_axial_symmetry', 'counter_quad_centrosymmetry_nesting_semi_centrosymmetry', 'x_axial_symmetry_nesting_x_axial_symmetry', 'x_axial_symmetry_nesting_semi_centrosymmetry', 'semi_centrosymmetry_nesting_x_axial_symmetry', 'semi_centrosymmetry_nesting_semi_centrosymmtry']:
			for i in range(0, 4):
				metaDetails.append(str(bin(eval('0x' + sha256_block[i][0])))[2:].zfill(4))
				metaDetails.append(str(bin(eval('0x' + sha256_block[i][2])))[2:].zfill(4))
		elif symmetry_method in ['quad_centrosymmetry_nesting_quad_centrosymmetry', 'quad_centrosymmetry_nesting_counter_quad_centrosymmetry', 'counter_quad_centrosymmetry_nesting_quad_centrosymmetry', 'counter_quad_centrosymmetry_nesting_counter_quad_centrosymmetry']:
			for i in range(0, 4):
				metaDetails.append(str(bin(eval('0x' + sha256_block[i][1])))[2:].zfill(4))
		
		metaInfo = {
		'metaDetails' : metaDetails, 
		'symmetry_method' : symmetry_method, 
		'foreground' : foreground, 
		'background' : background, 
		'hash' : 'sha256'
		}
		
		return metaInfo
		
	
	def meta_generator(self, metaInfo, x_len = 400, y_len = 400, block_len = 50):
		
		meta = ''

		if metaInfo['hash'] == 'md5':
			if metaInfo['symmetry_method'] in ['quad_centrosymmetry', 'counter_quad_centrosymmetry']:
				meta = Image.new('RGB', (x_len / 2, y_len / 2))
				blocks = ImageDraw.Draw(meta)
				x_count = 0
				y_count = 0
				for x in range(0, x_len / 2, block_len):
					for y in range(0, y_len / 2, block_len):
						blocks_poly = [(x, y), (x + block_len, y), (x + block_len, y + block_len), (x, y + block_len)]
						if metaInfo['metaDetails'][x_count][y_count] == '0':
							blocks.polygon(blocks_poly, fill = metaInfo['background'])
						else:
							blocks.polygon(blocks_poly, fill = metaInfo['foreground'])
						y_count += 1
					y_count = 0
					x_count += 1
				return {'meta' : meta, 'sym_info' : metaInfo['symmetry_method'], 'hash' : 'md5'}
			else:
				meta = Image.new('RGB', (x_len / 2, y_len))
				blocks = ImageDraw.Draw(meta)
				x_count = 0
				y_count = 0
				for x in range(0, x_len / 2, block_len):
					for y in range(0, y_len, block_len):
						blocks_poly = [(x, y), (x + block_len, y), (x + block_len, y + block_len), (x, y + block_len)]
						if metaInfo['metaDetails'][y_count][x_count] == '0':
							blocks.polygon(blocks_poly, fill = metaInfo['background'])
						else:
							blocks.polygon(blocks_poly, fill = metaInfo['foreground'])
						y_count += 1
					y_count = 0
					x_count += 1
				return {'meta' : meta, 'sym_info' : metaInfo['symmetry_method'], 'hash' : 'md5'}
		elif metaInfo['hash'] == 'sha256':
			block_len /= 2
			if metaInfo['symmetry_method'] in ['quad_centrosymmetry_nesting_quad_centrosymmetry', 'quad_centrosymmetry_nesting_counter_quad_centrosymmetry', 'counter_quad_centrosymmetry_nesting_quad_centrosymmetry', 'counter_quad_centrosymmetry_nesting_counter_quad_centrosymmetry']:
				meta = Image.new('RGB', (x_len / 4, y_len / 4))
				blocks = ImageDraw.Draw(meta)
				x_count = 0
				y_count = 0
				for x in range(0, x_len / 4, block_len):
					for y in range(0, y_len / 4, block_len):
						blocks_poly = [(x, y), (x + block_len, y), (x + block_len, y + block_len), (x, y + block_len)]
						if metaInfo['metaDetails'][x_count][y_count] == '0':
							blocks.polygon(blocks_poly, fill = metaInfo['background'])
						else:
							blocks.polygon(blocks_poly, fill = metaInfo['foreground'])
						y_count += 1
					y_count = 0
					x_count += 1
				return {'meta' : meta, 'sym_info' : metaInfo['symmetry_method'], 'hash' : 'sha256'}
			elif metaInfo['symmetry_method'] in ['quad_centrosymmetry_nesting_x_axial_symmetry', 'quad_centrosymmetry_nesting_semi_centrosymmetry', 'counter_quad_centrosymmetry_nesting_x_axial_symmetry', 'counter_quad_centrosymmetry_nesting_semi_centrosymmetry', 'x_axial_symmetry_nesting_x_axial_symmetry', 'x_axial_symmetry_nesting_semi_centrosymmetry', 'semi_centrosymmetry_nesting_x_axial_symmetry', 'semi_centrosymmetry_nesting_semi_centrosymmtry']:
				meta = Image.new('RGB', (x_len / 4, y_len / 2))
				blocks = ImageDraw.Draw(meta)
				x_count = 0
				y_count = 0
				for x in range(0, x_len / 4, block_len):
					for y in range(0, y_len / 2, block_len):
						blocks_poly = [(x, y), (x + block_len, y), (x + block_len, y + block_len), (x, y + block_len)]
						if metaInfo['metaDetails'][y_count][x_count] == '0':
							blocks.polygon(blocks_poly, fill = metaInfo['background'])
						else:
							blocks.polygon(blocks_poly, fill = metaInfo['foreground'])
						y_count += 1
					y_count = 0
					x_count += 1
				return {'meta' : meta, 'sym_info' : metaInfo['symmetry_method'], 'hash' : 'sha256'}
			elif metaInfo['symmetry_method'] in ['non_nesting_quad_centrosymmetry', 'non_nesting_counter_quad_centrosymmetry']:
				meta = Image.new('RGB', (x_len / 2, y_len / 2))
				blocks = ImageDraw.Draw(meta)
				x_count = 0
				y_count = 0
				for x in range(0, x_len / 2, block_len):
					for y in range(0, y_len / 2, block_len):
						blocks_poly = [(x, y), (x + block_len, y), (x + block_len, y + block_len), (x, y + block_len)]
						if metaInfo['metaDetails'][x_count][y_count] == '0':
							blocks.polygon(blocks_poly, fill = metaInfo['background'])
						else:
							blocks.polygon(blocks_poly, fill = metaInfo['foreground'])
						y_count += 1
					y_count = 0
					x_count += 1
				return {'meta' : meta, 'sym_info' : metaInfo['symmetry_method'], 'hash' : 'sha256'}
			elif metaInfo['symmetry_method'] in ['non_nesting_x_axial_symmetry', 'non_nesting_semi_centrosymmetry']:
				meta = Image.new('RGB', (x_len / 2, y_len))
				blocks = ImageDraw.Draw(meta)
				x_count = 0
				y_count = 0
				for x in range(0, x_len / 2, block_len):
					for y in range(0, y_len, block_len):
						blocks_poly = [(x, y), (x + block_len, y), (x + block_len, y + block_len), (x, y + block_len)]
						if metaInfo['metaDetails'][y_count][x_count] == '0':
							blocks.polygon(blocks_poly, fill = metaInfo['background'])
						else:
							blocks.polygon(blocks_poly, fill = metaInfo['foreground'])
						y_count += 1
					y_count = 0
					x_count += 1
				return {'meta' : meta, 'sym_info' : metaInfo['symmetry_method'], 'hash' : 'sha256'}


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
		
		if meta['hash'] == 'md5':
			if meta['sym_info'] == 'x_axial_symmetry':
				avatar = self.x_axial_symmetry(meta['meta'])
			elif meta['sym_info'] == 'counter_quad_centrosymmetry':
				avatar = self.counter_quad_centrosymmetry(meta['meta'])
			elif meta['sym_info'] == 'semi_centrosymmetry':
				avatar = self.semi_centrosymmetry(meta['meta'])
			elif meta['sym_info'] == 'quad_centrosymmetry':
				avatar = self.quad_centrosymmetry(meta['meta'])
		elif meta['hash'] == 'sha256':
			if meta['sym_info'] in ['non_nesting_x_axial_symmetry', 'quad_centrosymmetry_nesting_x_axial_symmetry', 'counter_quad_centrosymmetry_nesting_x_axial_symmetry', 'x_axial_symmetry_nesting_x_axial_symmetry', 'semi_centrosymmetry_nesting_x_axial_symmetry']:
				avatar = self.x_axial_symmetry(meta['meta'])
			if meta['sym_info'] in ['non_nesting_semi_centrosymmetry', 'quad_centrosymmetry_nesting_semi_centrosymmetry', 'counter_quad_centrosymmetry_nesting_semi_centrosymmetry', 'x_axial_symmetry_nesting_semi_centrosymmetry', 'semi_centrosymmetry_nesting_semi_centrosymmtry']:
				avatar = self.semi_centrosymmetry(meta['meta'])
			if meta['sym_info'] in ['non_nesting_quad_centrosymmetry', 'quad_centrosymmetry_nesting_quad_centrosymmetry', 'counter_quad_centrosymmetry_nesting_quad_centrosymmetry']:
				avatar = self.quad_centrosymmetry(meta['meta'])
			if meta['sym_info'] in ['non_nesting_counter_quad_centrosymmetry', 'quad_centrosymmetry_nesting_counter_quad_centrosymmetry', 'counter_quad_centrosymmetry_nesting_counter_quad_centrosymmetry']:
				avatar = self.counter_quad_centrosymmetry(meta['meta'])
			if meta['sym_info'] in ['quad_centrosymmetry_nesting_x_axial_symmetry', 'quad_centrosymmetry_nesting_semi_centrosymmetry', 'quad_centrosymmetry_nesting_quad_centrosymmetry', 'quad_centrosymmetry_nesting_counter_quad_centrosymmetry']:
				avatar = self.quad_centrosymmetry(avatar)
			if meta['sym_info'] in ['counter_quad_centrosymmetry_nesting_x_axial_symmetry', 'counter_quad_centrosymmetry_nesting_semi_centrosymmetry', 'counter_quad_centrosymmetry_nesting_quad_centrosymmetry', 'counter_quad_centrosymmetry_nesting_counter_quad_centrosymmetry']:
				avatar = self.counter_quad_centrosymmetry(avatar)
			if meta['sym_info'] in ['x_axial_symmetry_nesting_x_axial_symmetry', 'x_axial_symmetry_nesting_semi_centrosymmetry']:
				avatar = self.y_axial_symmetry(avatar)
				avatar = self.x_axial_symmetry(avatar)
			if meta['sym_info'] in ['semi_centrosymmetry_nesting_x_axial_symmetry', 'semi_centrosymmetry_nesting_semi_centrosymmtry']:
				avatar = self.y_axial_symmetry(avatar)
				avatar = self.semi_centrosymmetry(avatar)
		
		return avatar
	
	def y_axial_symmetry(self, meta):
		
		avatar = Image.new('RGB', (meta.size[0], meta.size[1] * 2))
		avatar.paste(meta, (0, 0))
		trans = meta.transpose(Image.FLIP_TOP_BOTTOM)
		avatar.paste(trans, (0, meta.size[1]))
		
		return avatar
	
	
	def x_axial_symmetry(self, meta):
		
		avatar = Image.new('RGB', (meta.size[0] * 2, meta.size[1]))
		avatar.paste(meta, (0, 0))
		trans = meta.transpose(Image.FLIP_LEFT_RIGHT)
		avatar.paste(trans, (meta.size[0], 0))
		
		return avatar
	
	def semi_centrosymmetry(self, meta):
		
		avatar = Image.new('RGB', (meta.size[0] * 2, meta.size[1]))
		avatar.paste(meta, (0, 0))
		avatar.paste(meta.rotate(180), (meta.size[0], 0))
		
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
		
	def cal_distance(self, p1, p2):
		
		hex1 = [int((hex(p1)[2:].zfill(6))[:2], 16), int((hex(p1)[2:].zfill(6))[2:4], 16), int((hex(p1)[2:].zfill(6))[4:6], 16)]
		hex2 = [int((hex(p2)[2:].zfill(6))[:2], 16), int((hex(p2)[2:].zfill(6))[2:4], 16), int((hex(p2)[2:].zfill(6))[4:6], 16)]		
		distance = 0.0
		sqr_sum = 0
		
		for i in range(0, len(hex1)):
			sqr_sum += (hex1[i] - hex2[i]) ** 2
		distance = math.sqrt(sqr_sum)
		
		return distance

if __name__ == '__main__':
	
	try:
		cf = ConfigParser.ConfigParser()
		cf.read('config.ini')
		cf_history = cf.get('options', 'history')
		if cf_history.lower() not in ['on', 'off']:
			exit()
	except:
		print "The file config.ini should be modified correctly before running the program."
		exit()

	if len(sys.argv) < 2:
		sys.argv.append(str(time.time()))
	ag = avatar_generator()
	
	meta = ''
	if len(sys.argv) >= 3:
		meta = ag.meta_generator(ag.str2meta_md5(sys.argv[1]))
	else:
		meta = ag.meta_generator(ag.str2meta_sha256(sys.argv[1]))
	avatar = ag.avatar_generator(meta)
	avatar.show()

	if cf_history.lower() == 'on':
		if not os.path.exists('history/'):
			os.makedirs('history/')
		if not os.path.exists('history/' + sys.argv[1] + '.jpg'):
			avatar.save('history/' + sys.argv[1] + '.jpg', 'JPEG')
