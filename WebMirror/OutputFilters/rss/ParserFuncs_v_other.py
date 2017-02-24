
# pylint: disable=C0112,R0911,R0912,W0612

from WebMirror.OutputFilters.util.MessageConstructors import buildReleaseMessage
from WebMirror.OutputFilters.util.TitleParsers import extractChapterVolFragment
from WebMirror.OutputFilters.util.TitleParsers import extractVolChapterFragmentPostfix

import re

####################################################################################################################################################
def extractYoraikun(item):
	'''
	# Yoraikun
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'The Rise of the Shield Hero' in item['tags']:
		return buildReleaseMessage(item, 'The Rise of the Shield Hero', vol, chp, frag=frag, postfix=postfix)
	elif 'Konjiki no Wordmaster' in item['tags']:
		return buildReleaseMessage(item, 'Konjiki no Wordmaster', vol, chp, frag=frag, postfix=postfix)
	elif 'IKCTAWBWTWH' in item['tags']:
		return buildReleaseMessage(item, 'I Kinda Came to Another World, But Where\'s the Way Home', vol, chp, frag=frag, postfix=postfix)
	elif 'Sevens' in item['tags']:
		return buildReleaseMessage(item, 'Sevens', vol, chp, frag=frag, postfix=postfix)
	elif 'The Lazy King' in item['tags']:
		return buildReleaseMessage(item, 'The Lazy King', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractYorasuTranslations(item):
	'''
	# Yoraikun
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if item['title'].startswith("DKFTOD"):
		return buildReleaseMessage(item, 'Devil King From The Otherworldly Dimension', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith("Hacker"):
		return buildReleaseMessage(item, 'Hacker', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith('Fallen God Records'):
		return buildReleaseMessage(item, 'Fallen God Records', vol, chp, frag=frag, postfix=postfix)

	if 'Godly Model Creator' in item['tags']:
		return buildReleaseMessage(item, 'Godly Model Creator', vol, chp, frag=frag, postfix=postfix)
	if 'Super Brain Telekinesis' in item['tags']:
		return buildReleaseMessage(item, 'Super Brain Telekinesis', vol, chp, frag=frag, postfix=postfix)
	if 'Super soldier' in item['tags']:
		return buildReleaseMessage(item, 'Super soldier', vol, chp, frag=frag, postfix=postfix)
	if 'The Different World Of Demon Lord' in item['tags']:
		return buildReleaseMessage(item, 'The Different World Of Demon Lord', vol, chp, frag=frag, postfix=postfix)
	return False



####################################################################################################################################################
def extractWuxiaworld(item):
	'''
	# Wuxiaworld

	'''
	chp, vol, frag = extractChapterVolFragment(item['title'])
	if not (chp or vol or frag):
		return False
	if 'Announcements' in item['tags']:
		return False

	if 'CD Chapter Release' in item['tags'] or 'Coiling Dragon' in item['tags']:
		return buildReleaseMessage(item, "Coiling Dragon", vol, chp, frag=frag)
	if 'dragon king with seven stars' in item['tags'] or 'Dragon King with Seven Stars' in item['title']:
		return buildReleaseMessage(item, "Dragon King with Seven Stars", vol, chp, frag=frag)
	if 'ISSTH Chapter Release' in item['tags'] or 'I Shall Seal the Heavens' in item['tags']:
		return buildReleaseMessage(item, "I Shall Seal the Heavens", vol, chp, frag=frag)
	if 'BTTH Chapter Release' in item['tags'] or 'BTTH Chapter' in item['title'] or 'Battle Through the Heavens' in item['tags']:
		return buildReleaseMessage(item, "Battle Through the Heavens", vol, chp, frag=frag)
	if 'SL Chapter Release' in item['tags'] or 'SA Chapter Release' in item['tags'] or 'Skyfire Avenue' in item['tags']:
		return buildReleaseMessage(item, "Skyfire Avenue", vol, chp, frag=frag)
	if 'MGA Chapter Release' in item['tags'] or 'Martial God Asura' in item['tags']:
		return buildReleaseMessage(item, "Martial God Asura", vol, chp, frag=frag)
	if 'ATG Chapter Release' in item['tags'] or 'Against the Gods' in item['tags']:
		return buildReleaseMessage(item, "Ni Tian Xie Shen", vol, chp, frag=frag)
	if 'ST Chapter Release' in item['tags']:
		return buildReleaseMessage(item, "Xingchenbian", vol, chp, frag=frag)
	if 'HJC Chapter Release' in item['tags'] or 'Heavenly Jewel Change' in item['tags']:
		return buildReleaseMessage(item, "Heavenly Jewel Change", vol, chp, frag=frag)
	if 'Child of Light' in item['tags'] or 'COL Chapter Release' in item['tags']:
		return buildReleaseMessage(item, 'Child of Light', vol, chp, frag=frag)
	if 'TDG Chapter Release' in item['tags'] or 'Tales of Demons & Gods' in item['tags']:
		return buildReleaseMessage(item, 'Tales of Demons & Gods', vol, chp, frag=frag)
	if 'TGR Chapter Release' in item['tags'] or 'The Great Ruler' in item['tags']:
		return buildReleaseMessage(item, 'The Great Ruler', vol, chp, frag=frag)
	if 'DE Chapter Release' in item['tags'] or 'Desolate Era' in item['tags']:
		return buildReleaseMessage(item, 'Desolate Era', vol, chp, frag=frag)
	if 'Wu Dong Qian Kun' in item['tags']:
		return buildReleaseMessage(item, 'Wu Dong Qian Kun', vol, chp, frag=frag)
	if 'Perfect World' in item['tags']:
		return buildReleaseMessage(item, 'Perfect World', vol, chp, frag=frag)
	if 'Gate of Revelation' in item['tags']:
		return buildReleaseMessage(item, 'The Gate of Revelation', vol, chp, frag=frag)
	if 'Upgrade Specialist in Another World' in item['tags']:
		return buildReleaseMessage(item, 'Upgrade Specialist in Another World', vol, chp, frag=frag)
	if 'Renegade Immortal' in item['tags']:
		return buildReleaseMessage(item, 'Renegade Immortal', vol, chp, frag=frag)
	if 'Sovereign of the Three Realms' in item['tags']:
		return buildReleaseMessage(item, 'Sovereign of the Three Realms', vol, chp, frag=frag)
	if 'Terror Infinity' in item['tags']:
		return buildReleaseMessage(item, 'Terror Infinity', vol, chp, frag=frag)
	if 'Warlock of the Magus World' in item['tags']:
		return buildReleaseMessage(item, 'Warlock of the Magus World', vol, chp, frag=frag)
	if 'Spirit Realm' in item['tags']:
		return buildReleaseMessage(item, 'Spirit Realm', vol, chp, frag=frag)
	if 'Rebirth of the Thief' in item['tags']:
		return buildReleaseMessage(item, 'Rebirth of the Thief', vol, chp, frag=frag)
	if "Emperor's Domination" in item['tags']:
		return buildReleaseMessage(item, "Emperor's Domination", vol, chp, frag=frag)
	if 'Upgrade Specialist' in item['tags']:
		return buildReleaseMessage(item, 'Upgrade Specialist', vol, chp, frag=frag)
	if 'A Will Eternal' in item['tags']:
		return buildReleaseMessage(item, 'A Will Eternal', vol, chp, frag=frag)
	if 'Absolute Choice' in item['tags']:
		return buildReleaseMessage(item, 'Absolute Choice', vol, chp, frag=frag)
	if 'Legend of the Dragon King' in item['tags']:
		return buildReleaseMessage(item, 'Legend of the Dragon King', vol, chp, frag=frag)

	return False




####################################################################################################################################################
def extractZiruTranslations(item):
	'''
	# Ziru's Musings | Translations~

	'''
	chp, vol, frag = extractChapterVolFragment(item['title'])

	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Dragon Bloodline' in item['tags'] or 'Dragon’s Bloodline — Chapter ' in item['title']:
		return buildReleaseMessage(item, 'Dragon Bloodline', vol, chp, frag=frag)
	if 'Lazy Dungeon Master' in item['tags'] or 'Lazy Dungeon Master ' in item['title']:
		return buildReleaseMessage(item, 'Lazy Dungeon Master', vol, chp, frag=frag)
	if 'Happy Peach' in item['tags'] or 'Happy Peach ' in item['title']:
		return buildReleaseMessage(item, 'Happy Peach', vol, chp, frag=frag)
	if "The Guild's Cheat Receptionist" in item['tags']:
		return buildReleaseMessage(item, "The Guild's Cheat Receptionist", vol, chp, frag=frag)
	if 'Suterareta Yuusha no Eiyuutan' in item['tags']:
		return buildReleaseMessage(item, 'Suterareta Yuusha no Eiyuutan', vol, chp, frag=frag)
	if 'The Restart' in item['tags']:
		return buildReleaseMessage(item, 'The Restart', vol, chp, frag=frag, tl_type='oel')

	# Wow, the tags must be hand typed. soooo many typos
	if 'Suterareta Yuusha no Eiyuutan' in item['tags'] or \
		'Suterareta Yuusha no Eyuutan' in item['tags'] or \
		'Suterurareta Yuusha no Eiyuutan' in item['tags']:

		extract = re.search(r'Suterareta Yuusha no Ei?yuutan \((\d+)\-(.+?)\)', item['title'])
		if extract:
			vol = int(extract.group(1))
			try:
				chp = int(extract.group(2))
				postfix = ''
			except ValueError:
				chp = None
				postfix = extract.group(2)
			return buildReleaseMessage(item, 'Suterareta Yuusha no Eiyuutan', vol, chp, postfix=postfix)
	return False



####################################################################################################################################################
def extractVoidTranslations(item):
	'''
	# Void Translations

	'''
	chp, vol, dummy_frag = extractChapterVolFragment(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	match = re.search(r'^Xian Ni Chapter \d+ ?[\-–]? ?(.*)$', item['title'])
	if match:
		return buildReleaseMessage(item, 'Xian Ni', vol, chp, postfix=match.group(1))

	return False




def extractXCrossJ(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Character Analysis' in item['title']:
		return False

	if 'Cross Gun' in item['tags']:
		return buildReleaseMessage(item, 'Cross Gun', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	if 'Konjiki no Moji Tsukai' in item['title']:
		postfix = item['title'].split(":", 1)[-1].strip()
		return buildReleaseMessage(item, 'Konjiki no Wordmaster', vol, chp, frag=frag, postfix=postfix)
	if 'Shinwa Densetsu no Eiyuu no Isekaitan' in item['tags']:
		return buildReleaseMessage(item, 'Shinwa Densetsu no Eiyuu no Isekaitan', vol, chp, frag=frag, postfix=postfix)
	if 'Isekai Mahou wa Okureteru' in item['tags']:
		return buildReleaseMessage(item, 'Isekai Mahou wa Okureteru', vol, chp, frag=frag, postfix=postfix)
	if  'Nidome no Jinsei wo Isekai de' in item['tags']:
		return buildReleaseMessage(item,  'Nidome no Jinsei wo Isekai de', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractWuxiaTranslations(item):
	'''
	# Wuxia Translations

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	releases = [
		'A Martial Odyssey',
		'Law of the Devil',
		'Tensei Shitara Slime Datta Ken',
		'The Nine Cauldrons',
		'Sovereign of the Three Realms',
	]
	for name in releases:
		if name in item['title'] and (chp or vol):
			return buildReleaseMessage(item, name, vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
def extract1HP(item):
	'''
	# 1HP

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Route to almightyness from 1HP' in item['title'] and (chp or vol):
		return buildReleaseMessage(item, 'HP1 kara Hajimeru Isekai Musou', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractWatermelons(item):
	'''
	# World of Watermelons

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	matches = re.search(r'\bB(\d+)C(\d+)\b', item['title'])
	if 'The Desolate Era' in item['tags'] and matches:
		vol, chp = matches.groups()
		postfix = ""
		if "–" in item['title']:
			postfix = item['title'].split("–", 1)[-1]

		return buildReleaseMessage(item, 'Mang Huang Ji', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
def extractWCCTranslation(item):
	'''
	# WCC Translation

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if "chapter" in item['title'].lower():
		if ":" in item['title']:
			postfix = item['title'].split(":", 1)[-1]
		return buildReleaseMessage(item, 'World Customize Creator', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
# 'yukkuri-literature-service'
####################################################################################################################################################
def extractYukkuri(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if '10 nen goshi no HikiNEET o Yamete Gaishutsushitara Jitaku goto Isekai ni Ten’ishiteta' in item['tags'] or \
		 'When I was going out from my house to stop become a Hiki-NEET after 10 years I was transported to another world' in item['tags'] or \
		 item['title'].startswith("10 nen goshi no HikiNEET o Yamete Gaishutsushitara Jitaku goto Isekai ni Ten’ishiteta"):
		return buildReleaseMessage(item, '10 nen goshi no HikiNEET o Yamete Gaishutsushitara Jitaku goto Isekai ni Ten’ishiteta', vol, chp, frag=frag, postfix=postfix)
	elif 'Takarakuji de 40 Oku Atattanda kedo Isekai ni Ijuusuru' in item['tags'] or \
		'Takarakuji de 40 Oku Atattanda kedo Isekai ni Ijuusuru.' in item['title']:
		return buildReleaseMessage(item, 'Takarakuji de 40 Oku Atattanda kedo Isekai ni Ijuusuru', vol, chp, frag=frag, postfix=postfix)
	elif 'Tenseisha wa Cheat o Nozomanai' in item['tags']:
		return buildReleaseMessage(item, 'Tenseisha wa Cheat o Nozomanai', vol, chp, frag=frag, postfix=postfix)
	elif 'Genjitsushugisha no Oukoku Kaizouki' in item['tags'] or item['title'].startswith("Genjitsushugisha no Oukoku Kaizouki"):
		return buildReleaseMessage(item, 'Genjitsushugisha no Oukoku Kaizouki', vol, chp, frag=frag, postfix=postfix)
	elif 'I Won 4 Billion in a Lottery But I Went to Another World' in item['tags']:
		return buildReleaseMessage(item, 'Takarakuji de 40 Oku Atattanda kedo Isekai ni Ijuusuru', vol, chp, frag=frag, postfix=postfix)
	elif 'Genjitsushugi Yuusha no Oukokusaikenki' in item['tags']:
		return buildReleaseMessage(item, 'Genjitsushugi Yuusha no Oukokusaikenki', vol, chp, frag=frag, postfix=postfix)
	elif 'Himekishi to Camping Car' in item['tags']:
		return buildReleaseMessage(item, 'Himekishi to Camping Car', vol, chp, frag=frag, postfix=postfix)
	elif 'Isekai de 『Kuro no Iyashite-tte』 Yobarete Imasu' in item['tags']:
		return buildReleaseMessage(item, 'Isekai de 『Kuro no Iyashite-tte』 Yobarete Imasu', vol, chp, frag=frag, postfix=postfix)
	elif  'The Curious Girl and The Traveler' in item['tags']:
		return buildReleaseMessage(item,  'The Curious Girl and The Traveler', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	elif  'Yukkuri Oniisan' in item['tags']:
		return buildReleaseMessage(item,  'Yukkuri Oniisan', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	elif  'The Valtras Myth' in item['tags']:
		return buildReleaseMessage(item,  'The Valtras Myth', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	elif item['title'].startswith("Our New World - Chapter"):
		return buildReleaseMessage(item,  'Our New World', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False


####################################################################################################################################################
#
####################################################################################################################################################
def extract87Percent(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Return of the former hero' in item['tags']:
		return buildReleaseMessage(item, 'Return of the Former Hero', vol, chp, frag=frag, postfix=postfix)
	if 'Dragon egg' in item['tags']:
		return buildReleaseMessage(item, 'Reincarnated as a dragon’s egg ～Lets aim to be the strongest～', vol, chp, frag=frag, postfix=postfix)

	if 'Summoning at random' in item['tags']:
		return buildReleaseMessage(item, 'Summoning at Random', vol, chp, frag=frag, postfix=postfix)

	if 'Legend' in item['tags']:
		return buildReleaseMessage(item, 'レジェンド', vol, chp, frag=frag, postfix=postfix)

	if 'Death game' in item['tags']:
		return buildReleaseMessage(item, 'The world is fun as it has become a death game', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractWuxiaSociety(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "/forum/viewtopic.php" in item['linkUrl']:
		return None


	if 'The Heaven Sword and Dragon Sabre' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'The Heaven Sword and Dragon Sabre', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractWuxiaHeroes(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'The Nine Cauldrons' in item['tags']:
		return buildReleaseMessage(item, 'The Nine Cauldrons', vol, chp, frag=frag, postfix=postfix)
	if 'Conquest' in item['tags']:
		return buildReleaseMessage(item, 'Conquest', vol, chp, frag=frag, postfix=postfix)
	if 'Blood Hourglass' in item['title']:
		return buildReleaseMessage(item, 'Blood Hourglass', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractYoujinsite(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if '[God & Devil World]' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Shenmo Xitong', vol, chp, frag=frag, postfix=postfix)

	if '[LBD&A]' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Line between Devil and Angel', vol, chp, frag=frag, postfix=postfix)

	if '[VW: Conquer the World]' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'VW: Conquering the World', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractYoushoku(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'The Other World Dining Hall' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'The Other World Dining Hall', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractZSW(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])

	if 'Shen Mu' in item['tags'] and (chp or vol):
		return buildReleaseMessage(item, 'Shen Mu', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractXantAndMinions(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) and not "prologue" in item['title'].lower():
		return False
	if 'LV999 Villager' in item['title']:
		return buildReleaseMessage(item, 'LV999 Villager', vol, chp, frag=frag, postfix=postfix)
	if 'Boundary Labyrinth and the Foreign Magician' in item['title']:
		return buildReleaseMessage(item, 'Boundary Labyrinth and the Foreign Magician', vol, chp, frag=frag, postfix=postfix)
	if 'The Bears Bear a Bare Kuma' in item['title'] or 'Kuma Kuma Kuma Bear' in item['title']:
		return buildReleaseMessage(item, 'Kuma Kuma Kuma Bear', vol, chp, frag=frag, postfix=postfix)
	if "Black Knight" in item['title']:
		return buildReleaseMessage(item, "The Black Knight Who Was Stronger than even the Hero", vol, chp, frag=frag, postfix=postfix)
	if "Astarte’s Knight" in item['title']:
		return buildReleaseMessage(item, "Astarte's Knight", vol, chp, frag=frag, postfix=postfix)
	if "Queen’s Knight Kael" in item['title']:
		return buildReleaseMessage(item, "Queen's Knight Kael", vol, chp, frag=frag, postfix=postfix)
	if "Legend of Xingfeng" in item['title']:
		return buildReleaseMessage(item, "Legend of Xingfeng", vol, chp, frag=frag, postfix=postfix)
	if "iseiza" in item['tags']:
		return buildReleaseMessage(item, "Isekai Izakaya Nobu", vol, chp, frag=frag, postfix=postfix)
	if "NPWC" in item['tags']:
		return buildReleaseMessage(item, "New Theory – Nobusada’s Parallel World Chronicle", vol, chp, frag=frag, postfix=postfix)


	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractWatDaMeow(item):
	'''

	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Commushou' in item['tags']:
		return buildReleaseMessage(item, 'Commushou no Ore ga, Koushou Skill ni Zenfurishite Tenseishita Kekka', vol, chp, frag=frag, postfix=postfix)
	if 'Kitsune-sama' in item['tags']:
		return buildReleaseMessage(item, 'Isekai Kichattakedo Kaerimichi doko?', vol, chp, frag=frag, postfix=postfix)
	if "We live in dragon's peak" in item['tags']:
		return buildReleaseMessage(item, "We live in dragon's peak", vol, chp, frag=frag, postfix=postfix)
	if 'JuJoku' in item['title']:
		return buildReleaseMessage(item, 'Junai X Ryoujoku Kompurekusu', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractWolfieTranslation(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'The amber sword' in item['tags']:
		return buildReleaseMessage(item, 'The Amber Sword', vol, chp, frag=frag, postfix=postfix)
	if 'The latest game is too amazing' in item['tags']:
		return buildReleaseMessage(item, 'The Latest Game is too Amazing', vol, chp, frag=frag, postfix=postfix)
	if 'The strategy to become good at magic' in item['tags']:
		return buildReleaseMessage(item, 'The Strategy to Become Good at Magic', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractVerathragana(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if "Chapter" in item['title']:
		return buildReleaseMessage(item, 'The Prince Of Nilfheim', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractWitchLife(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Witch Life' in item['tags']:
		return buildReleaseMessage(item, 'Witch Life', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

	return False

####################################################################################################################################################
#
####################################################################################################################################################
def extractWalkingTheStorm(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	return buildReleaseMessage(item, "Joy of life", vol, chp, frag=frag, postfix=postfix)


####################################################################################################################################################
#
####################################################################################################################################################
def extractWebNovelJapaneseTranslation(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Kizoku Yamemasu Shomin ni Narimasu' in item['tags']:
		return buildReleaseMessage(item, 'Kizoku Yamemasu Shomin ni Narimasu', vol, chp, frag=frag, postfix=postfix)

	return False








def  extractWeleTranslation(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if item['title'].lower().startswith('sin city'):
		return buildReleaseMessage(item, 'Sin City', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('zhan xian'):
		return buildReleaseMessage(item, 'Zhan Xian', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('heaven awakening path'):
		return buildReleaseMessage(item, 'Heaven Awakening Path', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('immortal executioner'):
		return buildReleaseMessage(item, 'Immortal Executioner', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################

def  extractWalkTheJiangHu(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'TTNH Chapter' in item['title']:
		return buildReleaseMessage(item, "Transcending the Nine Heavens", vol, chp, frag=frag, postfix=postfix)
	return False

####################################################################################################################################################
#
####################################################################################################################################################

def  extractYiYueTranslation(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractZxzxzxsBlog(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def  extract一期一会万歳(item):
	'''
	# '一期一会, 万歳!'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def  extractWhenTheHuntingPartyCame(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractXiaowen206sBlog(item):
	'''
	# "Xiaowen206's Blog"
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractWhiteTigerTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if item['title'].lower().startswith('mp volume'):
		return buildReleaseMessage(item, 'Martial Peak', vol, chp, frag=frag, postfix=postfix)
	if item['title'].lower().startswith('ipash chapter'):
		return buildReleaseMessage(item, 'Martial Peak', vol, chp, frag=frag, postfix=postfix)

	return False

def  extractWhiteNightSite(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'What Came to Mind During My Third Time in Another World Was to for Now, Get Naked.' in item['tags']:
		return buildReleaseMessage(item, 'What Came to Mind During My Third Time in Another World Was to for Now, Get Naked.', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################

def  extractZombieKnight(item):
	'''

	'''
	titleconcat = " ".join(item['tags']) + item['title']
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(titleconcat)
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	return buildReleaseMessage(item, 'The Zombie Knight', vol, chp, frag=frag, postfix=postfix, tl_type='oel')

####################################################################################################################################################
#
####################################################################################################################################################

def  extractWuxiwish(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractWIP(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	print(item['title'])
	print(item['tags'])
	print("'{}', '{}', '{}', '{}'".format(vol, chp, frag, postfix))

	return False






####################################################################################################################################################
#
####################################################################################################################################################

def  extractZenTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractWorldofSummie(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractWizThiefsNovels(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'My immortality It’s in a Death game' in item['title']:
		return buildReleaseMessage(item, 'My immortality It\'s in a Death game', vol, chp, frag=frag, postfix=postfix)
	if 'Thanks to a different world reincarnation' in item['title']:
		return buildReleaseMessage(item, 'Thanks to a different world reincarnation', vol, chp, frag=frag, postfix=postfix)
	if 'Grave “Z”' in item['title']:
		return buildReleaseMessage(item, 'Grave "Z"', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractVillageTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractWuxiaTranslators(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'World Defying Dan God' in item['tags']:
		return buildReleaseMessage(item, 'World Defying Dan God', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractWillfulCasual(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Chu Wang Fei' in item['tags']:
		return buildReleaseMessage(item, "Chu Wang Fei", vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################

def  extractVolareTranslations(item):
	'''
	'Volare Translations'
	also
	'Volare Novels'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Great Demon King' in item['tags']:
		return buildReleaseMessage(item, 'Great Demon King', vol, chp, frag=frag, postfix=postfix)
	if 'Sovereign of the Three Realms' in item['tags']:
		return buildReleaseMessage(item, 'Sovereign of the Three Realms', vol, chp, frag=frag, postfix=postfix)
	if 'Age of Lazurite' in item['tags']:
		return buildReleaseMessage(item, 'Age of Lazurite, Tower of Glass', vol, chp, frag=frag, postfix=postfix)
	if 'Apartment from Hell' in item['tags']:
		return buildReleaseMessage(item, "Apartment from Hell", vol, chp, frag=frag, postfix=postfix)
	if 'Celestial Employee' in item['tags']:
		return buildReleaseMessage(item, "Celestial Employee", vol, chp, frag=frag, postfix=postfix)
	if 'Cultivation Chat Group' in item['tags']:
		return buildReleaseMessage(item, "Cultivation Chat Group", vol, chp, frag=frag, postfix=postfix)
	if 'Falling Dreams of Fang Hua' in item['tags']:
		return buildReleaseMessage(item, "Falling Dreams of Fang Hua", vol, chp, frag=frag, postfix=postfix)
	if 'My Wife is a Beautiful CEO' in item['tags']:
		return buildReleaseMessage(item, "My Wife is a Beautiful CEO", vol, chp, frag=frag, postfix=postfix)
	if 'Release that Witch' in item['tags']:
		return buildReleaseMessage(item, "Release that Witch", vol, chp, frag=frag, postfix=postfix)
	if 'Sword Spirit' in item['tags']:
		return buildReleaseMessage(item, "Sword Spirit", vol, chp, frag=frag, postfix=postfix)
	if "Demon Wang's Favorite Fei" in item['tags']:
		return buildReleaseMessage(item, "Demon Wang's Golden Favorite Fei", vol, chp, frag=frag, postfix=postfix)
	if 'True Cultivators' in item['tags']:
		return buildReleaseMessage(item, 'The Strong, The Few, True Cultivators on Campus', vol, chp, frag=frag, postfix=postfix)
	if "Evil Emperor's Wild Consort" in item['tags']:
		return buildReleaseMessage(item, "Evil Emperor's Wild Consort", vol, chp, frag=frag, postfix=postfix)
	if 'Star Rank Hunter' in item['tags']:
		return buildReleaseMessage(item, 'Star Rank Hunter', vol, chp, frag=frag, postfix=postfix)
	if 'Blood Hourglass' in item['tags']:
		return buildReleaseMessage(item, 'Blood Hourglass', vol, chp, frag=frag, postfix=postfix)

	if 'Special Forces Spirit' in item['tags']:
		return buildReleaseMessage(item, 'Special Forces Spirit', vol, chp, frag=frag, postfix=postfix)
	if 'Fleeting Midsummer' in item['tags']:
		return buildReleaseMessage(item, 'Fleeting Midsummer', vol, chp, frag=frag, postfix=postfix)
	if 'Poison Genius Consort' in item['tags']:
		return buildReleaseMessage(item, 'Poison Genius Consort', vol, chp, frag=frag, postfix=postfix)
	if 'Gourmet Food Supplier' in item['tags']:
		return buildReleaseMessage(item, 'Gourmet Food Supplier', vol, chp, frag=frag, postfix=postfix)
	if 'Hidden Marriage' in item['tags']:
		return buildReleaseMessage(item, 'Hidden Marriage', vol, chp, frag=frag, postfix=postfix)
	if "History's Strongest Senior Brother" in item['tags']:
		return buildReleaseMessage(item, "History's Strongest Senior Brother", vol, chp, frag=frag, postfix=postfix)
	if "I'm Hui Tai Lang" in item['tags']:
		return buildReleaseMessage(item, "I'm Hui Tai Lang", vol, chp, frag=frag, postfix=postfix)
	if 'Pivot of the Sky' in item['tags']:
		return buildReleaseMessage(item, 'Pivot of the Sky', vol, chp, frag=frag, postfix=postfix)
	if 'Poisoning the World' in item['tags']:
		return buildReleaseMessage(item, 'Poisoning the World: The Secret Service Mysterious Doctor is a Young Beastly Wife', vol, chp, frag=frag, postfix=postfix)


	if 'King of Hell' in item['tags']:
		return buildReleaseMessage(item, 'King of Hell', vol, chp, frag=frag, postfix=postfix)
	if 'Prodigal Alliance Head' in item['tags']:
		return buildReleaseMessage(item, 'Prodigal Alliance Head', vol, chp, frag=frag, postfix=postfix)




	return False

####################################################################################################################################################
#
####################################################################################################################################################

def  extractZeonic(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extract天才創造すなわち百合(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractWhimsicalLand(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extract12Superlatives(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractWeavingstoriesandbuildingcastlesintheclouds(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractWelcomeToTheUnderdark(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extract輝く世界(item):
	'''
	# '輝く世界'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def  extractYoutsubasilversBlog(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractWatermelonHelmets(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False
	if 'Dragon Life' in item['tags'] or 'Dragon Life: Chapter' in item['title']:
		return buildReleaseMessage(item, 'Dragon Life', vol, chp, frag=frag, postfix=postfix)

	return False

####################################################################################################################################################
#
####################################################################################################################################################

def  extractXantDoesStuffAndThings(item):
	'''
	# 'Xant Does Stuff and Things'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractXantbos(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extractWordofCraft(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Toaru Ossan no VRMMO katsudouki' in item['tags']:
		return buildReleaseMessage(item, 'Toaru Ossan no VRMMO katsudouki', vol, chp, frag=frag, postfix=postfix)
	return False

def  extractWLTranslations(item):
	'''
	# 'WL Translations'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Chapter Releases' in item['tags'] and ('OSI' in item['tags'] or item['title'].startswith("OSI Chapter")):
		return buildReleaseMessage(item, 'One Sword to Immortality', vol, chp, frag=frag, postfix=postfix)
	return False

def  extract睡眠中毒(item):
	'''
	# '睡眠中毒'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def  extractYoukoAdvent(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	# No chapter numbers in titles. Arrrgh

	return False

def  extractWormACompleteWebSerial(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def  extract7DaysTrial(item):
	'''
	#'7 Days Trial'
	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'content' in item['tags']:
		return buildReleaseMessage(item, 'War of the Supreme', vol, chp, frag=frag, postfix=postfix)
	return False


def  extract77Novel(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractWishUponAHope(item):
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractWumsTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractXianxiaTales(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractYamiTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Tensei Shoujo no Rirekisho' in item['tags']:
		return buildReleaseMessage(item, 'Tensei Shoujo no Rirekisho', vol, chp, frag=frag, postfix=postfix)

	return False
def extractZeroTranslations(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractV7Silent(item):
	'''

	'''
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None

	if 'The Demon Queen is My Fiancée!' in item['tags']:
		return buildReleaseMessage(item, 'The Demon Queen is My Fiancée!', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	if 'Getcha Skills' in item['tags']:
		return buildReleaseMessage(item, 'Getcha Skills', vol, chp, frag=frag, postfix=postfix, tl_type='oel')
	return False


def extractWarriorWriting(item):
	"""
	Warrior Writing
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractWigglyTranslation(item):
	"""
	Wiggly Translation
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if item['title'].startswith("Man Huang Feng Bao: "):
		return buildReleaseMessage(item, 'Man Huang Feng Bao', vol, chp, frag=frag, postfix=postfix)
	return False
def extractWorldofHope(item):
	"""
	World of Hope
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractWorldTurtleTranslations(item):
	"""
	World Turtle Translations
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractYasashiHonyaku(item):
	"""
	Yasashi Honyaku
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractYeagdrasil(item):
	"""
	Yeagdrasil
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extractYourMajestyPleaseCalmDown(item):
	"""
	Your Majesty Please Calm Down
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extract書櫃(item):
	"""
	『書櫃』
	"""

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False
def extract閒人ONLINE(item):
	"""
	閒人 • O N L I N E
	"""
	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'Great Tang Idyll' in item['tags']:
		return buildReleaseMessage(item, 'Great Tang Idyll', vol, chp, frag=frag, postfix=postfix)
	return False


def extractVeeTranslation(item):
	'''
	Vee Translation
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractVestigeTranslations(item):
	'''
	Vestige Translations
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractWhateverTranslationsMTL(item):
	'''
	Whatever Translations MTL
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractWisteriaTranslations(item):
	'''
	Wisteria Translations
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractWuxiaLovers(item):
	'''
	Wuxia Lovers
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if item['title'].startswith("CGA Chapter"):
		return buildReleaseMessage(item, 'Conquer God, Asura, and 1000 Beauties', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith("Etranger Chapter"):
		return buildReleaseMessage(item, 'Etranger', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith("Q11 Chapter"):
		return buildReleaseMessage(item, 'Queen of No.11 Agent 11', vol, chp, frag=frag, postfix=postfix)
	if item['title'].startswith("STS Chapter"):
		return buildReleaseMessage(item, '', vol, chp, frag=frag, postfix=postfix)
	return False

def extractXiakeluojiao侠客落脚(item):
	'''
	Xiakeluojiao 侠客落脚
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractXianXiaWorld(item):
	'''
	Xian Xia World
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'www.xianxiaworld.net/A-Thought-Through-Eternity/' in item['linkUrl']:
		return buildReleaseMessage(item, 'A Thought Through Eternity', vol, chp, frag=frag, postfix=postfix)
	if 'www.xianxiaworld.net/Beast-Piercing-The-Heavens/' in item['linkUrl']:
		return buildReleaseMessage(item, 'Beast Piercing The Heavens', vol, chp, frag=frag, postfix=postfix)
	if 'www.xianxiaworld.net/Dominating-Sword-Immortal/' in item['linkUrl']:
		return buildReleaseMessage(item, 'Dominating Sword Immortal', vol, chp, frag=frag, postfix=postfix)
	if 'www.xianxiaworld.net/Dragon-Marked-War-God/' in item['linkUrl']:
		return buildReleaseMessage(item, 'Dragon-Marked War God', vol, chp, frag=frag, postfix=postfix)
	if 'www.xianxiaworld.net/Emperor-of-The-Cosmos/' in item['linkUrl']:
		return buildReleaseMessage(item, 'Emperor of The Cosmos', vol, chp, frag=frag, postfix=postfix)
	if 'www.xianxiaworld.net/God-of-Slaughter/' in item['linkUrl']:
		return buildReleaseMessage(item, 'God of Slaughter', vol, chp, frag=frag, postfix=postfix)
	if 'www.xianxiaworld.net/God-level-Bodyguard-in-The-City/' in item['linkUrl']:
		return buildReleaseMessage(item, 'God-level Bodyguard in The City', vol, chp, frag=frag, postfix=postfix)
	if 'www.xianxiaworld.net/Realms-In-The-Firmament/' in item['linkUrl']:
		return buildReleaseMessage(item, 'Realms In The Firmament', vol, chp, frag=frag, postfix=postfix)
	if 'www.xianxiaworld.net/The-King-Of-Myriad-Domains/' in item['linkUrl']:
		return buildReleaseMessage(item, 'The King Of Myriad Domains', vol, chp, frag=frag, postfix=postfix)
	if 'www.xianxiaworld.net/The-Magus-Era/' in item['linkUrl']:
		return buildReleaseMessage(item, 'The Magus Era', vol, chp, frag=frag, postfix=postfix)
	if 'www.xianxiaworld.net/The-Portal-of-Wonderland/' in item['linkUrl']:
		return buildReleaseMessage(item, 'The Portal of Wonderland', vol, chp, frag=frag, postfix=postfix)
	if 'www.xianxiaworld.net/World-Defying-Dan-God/' in item['linkUrl']:
		return buildReleaseMessage(item, 'World Defying Dan God', vol, chp, frag=frag, postfix=postfix)

	return False

def extractXiaoyuusTranslations(item):
	'''
	Xiaoyuu\'s Translations
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False

def extractYumeabyss(item):
	'''
	Yumeabyss
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if "Black Bellied Prince's Stunning Abandoned Consort" in item['tags']:
		return buildReleaseMessage(item, "Black Bellied Prince's Stunning Abandoned Consort", vol, chp, frag=frag, postfix=postfix)
	if 'The Cry of the Phoenix Which Reached the Ninth Heaven' in item['tags']:
		return buildReleaseMessage(item, 'The Cry of the Phoenix Which Reached the Ninth Heaven', vol, chp, frag=frag, postfix=postfix)
	if 'Island: End of Nightmare' in item['tags']:
		return buildReleaseMessage(item, 'Island: End of Nightmare', vol, chp, frag=frag, postfix=postfix)
	if 'Xiao Qi, Wait' in item['tags']:
		return buildReleaseMessage(item, 'Xiao Qi, Wait', vol, chp, frag=frag, postfix=postfix)
	return False




def extractVersatileGuy(item):
	'''
	'Versatile Guy'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractWhiteleafTribe(item):
	'''
	'Whiteleaf Tribe'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractWinterTranslates(item):
	'''
	'Winter Translates'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractWorkingNEETTranslation(item):
	'''
	'Working NEET Translation'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractWorksofKun(item):
	'''
	'Works of Kun'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractWuxiaNation(item):
	'''
	'WuxiaNation'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None

	if 'the dark king' in item['tags']:
		return buildReleaseMessage(item, 'The Dark King', vol, chp, frag=frag, postfix=postfix)
	if 'age of heroes' in item['tags']:
		return buildReleaseMessage(item, 'Age of Heroes', vol, chp, frag=frag, postfix=postfix)
	if 'Conquer God, Asura, and 1000 Beauties' in item['tags']:
		return buildReleaseMessage(item, 'Conquer God, Asura, and 1000 Beauties', vol, chp, frag=frag, postfix=postfix)
	if 'The Solitary Sword Sovereign' in item['tags']:
		return buildReleaseMessage(item, 'The Solitary Sword Sovereign', vol, chp, frag=frag, postfix=postfix)
	if 'lord shadow' in item['tags']:
		return buildReleaseMessage(item, 'Lord Shadow', vol, chp, frag=frag, postfix=postfix)

	return False


def extractNepustation(item):
	'''
	'www.nepustation.com'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractXianForeigners(item):
	'''
	'Xian Foreigners'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	if 'President Wife Is A Man' in item['tags']:
		return buildReleaseMessage(item, 'President Wife Is A Man', vol, chp, frag=frag, postfix=postfix)
	return False


def extractYamtl(item):
	'''
	'yamtl'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractYuanshusCave(item):
	'''
	"Yuanshu's Cave"
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None

	if 'id' in item['tags']:
		return buildReleaseMessage(item, 'Id Fusion Story & Fantasy', vol, chp, frag=frag, postfix=postfix)



	return False


def extractYuNSTranslations(item):
	'''
	'yuNS Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extractZaelumTranslations(item):
	'''
	'Zaelum Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extract不法之徒LawlessGangster(item):
	'''
	'《不法之徒》 Lawless Gangster'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False


def extract愛主の翻訳AinushiTranslations(item):
	'''
	'愛主の翻訳  Ainushi Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol or frag) or "preview" in item['title'].lower():
		return None
	return False






def extractVariousTranslatedWork(item):
	'''
	Parser for 'Various Translated Work'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractVesperlxd(item):
	'''
	Parser for 'VesperLxD'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if 'Invincible Level Up' in item['tags']:
		return buildReleaseMessage(item,'Invincible Level Up', vol, chp, frag=frag, postfix=postfix)
	if 'Rebirth of an Abandoned Woman' in item['tags']:
		return buildReleaseMessage(item,'Rebirth of an Abandoned Woman', vol, chp, frag=frag, postfix=postfix)
	if "Great Han's Female General Wei Qiqi" in item['tags']:
		return buildReleaseMessage(item,"Great Han's Female General Wei Qiqi", vol, chp, frag=frag, postfix=postfix)

	return False



def extractVesperlxdTranslation(item):
	'''
	Parser for 'VesperLxD Translation'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractVgperson(item):
	'''
	Parser for 'VgPerson'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractWattpad(item):
	'''
	Parser for 'Wattpad'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractWeabooDesu(item):
	'''
	Parser for 'Weaboo Desu'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractWelcomeToTheMalformedBox(item):
	'''
	Parser for 'Welcome to the Malformed Box'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractWeleTranslations(item):
	'''
	Parser for 'Wele Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractWiegenliedOfGreen(item):
	'''
	Parser for 'Wiegenlied of Green'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractWuwuwu555(item):
	'''
	Parser for 'Wuwuwu555'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractWuxiaFantasies(item):
	'''
	Parser for 'Wuxia Fantasies'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractWuxiaWorld(item):
	'''
	Parser for 'Wuxia World'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractXcrossjTranslations(item):
	'''
	Parser for 'XCrossJ Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractYametteTranslations(item):
	'''
	Parser for 'Yamette Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractYorasuNovels(item):
	'''
	Parser for 'Yorasu Novels'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractYuujinchou(item):
	'''
	Parser for 'Yuujinchou'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractZazaTranslations(item):
	'''
	Parser for 'ZAZA Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractZips_17(item):
	'''
	Parser for 'Zips_17'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractZxzxzxSBlog(item):
	'''
	Parser for 'Zxzxzx's Blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractDevildante777SBlog(item):
	'''
	Parser for 'devildante777's Blog'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractOmgitsarayTranslations(item):
	'''
	Parser for 'omgitsaray translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractPanisal(item):
	'''
	Parser for 'panisal'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractTekuteku(item):
	'''
	Parser for 'tekuteku'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractTherabbitknight(item):
	'''
	Parser for 'therabbitknight'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractWeedsroyalroad(item):
	'''
	Parser for 'weedsroyalroad'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extractYenney(item):
	'''
	Parser for '♥ yenney ♥'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extract人见人爱的Sushi公主(item):
	'''
	Parser for '人见人爱的Sushi公主'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extract夢見る世界(item):
	'''
	Parser for '夢見る世界'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extract宿命の二人(item):
	'''
	Parser for '宿命の二人'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extract未完待续(item):
	'''
	Parser for '未完待续'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extract止めないでお姉さま(item):
	'''
	Parser for '止めないで、お姉さま…'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extract鏡像翻訳(item):
	'''
	Parser for '鏡像翻訳'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extract陽光的夏天(item):
	'''
	Parser for '陽光的夏天'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extract青玄豆腐幇(item):
	'''
	Parser for '青玄豆腐幇'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extract희노애락(item):
	'''
	Parser for '희노애락'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



def extract50Translations(item):
	'''
	Parser for '50% Translations'
	'''

	vol, chp, frag, postfix = extractVolChapterFragmentPostfix(item['title'])
	if not (chp or vol) or "preview" in item['title'].lower():
		return False

	if "WATTT" in item['tags']:
		return buildReleaseMessage(item, "WATTT", vol, chp, frag=frag, postfix=postfix)

	return False



