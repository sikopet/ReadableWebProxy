
GLOBAL_BAD_URLS = [
			'//mail.google.com',
			'/comments/feed/',
			'/embed?',
			'/osd.xml',
			'/page/page/',
			'/wp-json/',
			'/wp-login.php',
			'/xmlrpc.php',
			'?openidserver=1',
			'a.wikia-beacon.com',
			'accounts.google.com',
			'add.my.yahoo.com',
			'addtoany.com',
			'b.scorecardresearch.com',
			'delicious.com',
			'digg.com',
			'edit.yahoo.com',
			'facebook.com',
			'fbcdn-',
			'feeds.wordpress.com',
			'gprofiles.js',
			'javascript:void',
			'netvibes.com',
			'newsgator.com',
			'paypal.com',
			'pixel.wp.com',
			'public-api.wordpress.com',
			'r-login.wordpress.com',
			'reddit.com',
			'stumbleupon.com',
			'technorati.com',
			'topwebfiction.com',
			'twitter.com',
			'twitter.com/intent/',
			'wretch.cc',
			'ws-na.amazon-adsystem.com',
			'www.addtoany.com'
			'www.pinterest.com/pin/',
			'www.wattpad.com/login?',
			'www.tumblr.com/reblog/',

			'www.paypalobjects.com',

			# Tumblr can seriously go fuck itself with a rusty stake
			'tumblr.com/widgets/',
			'www.tumblr.com/login',
			'://tumblr.com',
			'&share=tumblr',

			'/wp-content/plugins/',
			'/wp-content/themes/',
			'/wp-json/oembed/',

			# At least one site (booksie) is serving the favicon with a mime-type
			# of "text/plain", which then confuses the absolute crap out of the
			# mime-type dispatcher.
			# Since I'm not re-serving favicons anyways, just do not fetch them ever.
			'favicon.ico',

			# Try to not scrape inline images
			';base64,',

			"www.fashionmodeldirectory.com",
			"www.watchingprivatepractice.com",
			"Ebonyimages.jupiterimages.com",

			# More garbage issues.
			'"https',
			'#comment-',
			'/oembed/1.0/',
			'&share=',
			'replytocom=',
			'?feed=rss2&page_id',
			'?share=tumblr',
			'?share=facebook',

			'chasingadreamtranslations.com/?fp=',

			# NFI where /this/ came from
			'www.miforcampuspolice.com',
			'tracking.feedpress.it',

			'www.quantcast.com',

			'mailto:',
			'javascript:popupWindow(',

			'en.blog.wordpress.com',

			'counter.yadro.ru',


			'/js/js/',
			'/css/css/',
			'/images/images/',
			'ref=dp_brlad_entry',
			'https:/www.',
			'tumblr.com/oembed/1.0?',
	]


GLOBAL_DECOMPOSE_BEFORE = [
			{'name'     : 'likes-master'},  # Bullshit sharing widgets
			{'id'       : 'jp-post-flair'},
			{'class'    : 'post-share-buttons'},
			#{'class'    : 'commentlist'},  # Scrub out the comments so we don't try to fetch links from them
			#{'class'    : 'comments'},
			#{'id'       : 'comments'},
		]

GLOBAL_DECOMPOSE_AFTER = []


RSS_SKIP_FILTER = [
	"www.baka-tsuki.org",
	"re-monster.wikia.com",
	'inmydaydreams.com',
	'www.fanfiction.net',
	'www.booksie.com',
	'www.booksiesilk.com',
	'www.fictionpress.com',
	'storiesonline.net',
	'www.fictionmania.tv',
	'www.bestories.net',
	'www.tgstorytime.com',
	'www.nifty.org',
	'www.literotica.com',
	'pokegirls.org',
	'www.asstr.org',
	'www.mcstories.com',
	'www.novelupdates.com',
	'40pics.com',
	'#comment-',
	'?showComment=',



]


RSS_TITLE_FILTER = [
	"by: ",
	"comments on: ",
	"comment on: ",
	"comment on ",
]


# Goooooo FUCK YOURSELF
GLOBAL_INLINE_BULLSHIT = [

			"This translation is property of Infinite Novel Translations.",
			"This translation is property of Infinite NovelTranslations.",
			"If you read this anywhere but at Infinite Novel Translations, you are reading a stolen translation.",
			"&lt;Blank&gt;",
			"&lt;space&gt;",
			"<Blank>",
			"<Blank>",
			"please read only translator’s websitewww.novitranslation.com",
			"please read only translator’s website www.novitranslation.com",
			"Please do not host elsewhere but MBC and Yumeabyss",
			'Original and most updated translations are from volaretranslations.',
			'Please support the translator for Wild Consort by reading on volarenovels!',
			'Original and most updated translations are from volaretranslations.',
			'Original and most updated translations are from volaretranslations.',
			"&lt;StarveCleric&gt;",
			'(trytranslations.com at your service!)',
			'Please do not host elsewhere but volare and Yumeabyss',
			'[Follow the latest chapter at wuxiadream.com]',

			'I slid my penis inside her. She squirmed a bit but YOU SICK FUCK STOP STEALING MY TRANSLATIONS',   # siiiiigh
			'I kissed her sweet anus once more before leaving',   # siiiiiiiiiiiiigh

			'(Watermark: read this translation only at shinku. xiaoxiaonovels.com)',
			"<TLN: If you're reading this novel at any other site than Sousetsuka.com you might be reading an unedited, uncorrected version of the novel.>",

			'Original and most updated translations are from volare. If read elsewhere, this chapter has been stolen. Please stop supporting theft.',
			'*******If you are reading this on a place other than rinkagetranslation.com, this chapter has been stolen and is neither the most recent or complete chapter.*******',
			'*******Read the chapters at rinkagetranslation.com. The chapters for this series will NOT be posted anywhere else other than on that site itself. If you are reading this from somewhere else then this is chapter has been stolen.*******',
			'If you are reading this on a place other than rinkagetranslation.com, this chapter has been stolen and is neither the most recent or complete chapter.',

			"Read The Lazy Swordmaster first on Lightnovelbastion.com (If you're reading this elsewhere, it has been stolen)",
			"Read The Lazy Swordmaster on Lightnovelbastion.com",

			"Property of © Fantasy-Books.live; outside of it, it is stolen.",

]
