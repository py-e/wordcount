# from https://en.wikipedia.org/wiki/Most_common_words_in_English
top_100_english_words = {
    'the': [1, 'Article'],
    'be': [2, 'Verb'],
    'to': [3, 'Preposition'],
    'of': [4, 'Preposition'],
    'and': [5, 'Conjunction'],
    'a': [6, 'Article'],
    'in': [7, 'Preposition'],
    'that': [8, 'Conjunction et al.'],
    'have': [9, 'Verb'],
    'i': [10, 'Pronoun'],
    'it': [11, 'Pronoun'],
    'for': [12, 'Preposition'],
    'not': [13, 'Adverb et al.'],
    'on': [14, 'Preposition'],
    'with': [15, 'Preposition'],
    'he': [16, 'Pronoun'],
    'as': [17, 'Adverb, conjunction, et al.'],
    'you': [18, 'Pronoun'],
    'do': [19, 'Verb, noun'],
    'at': [20, 'Preposition'],
    'this': [21, 'Determiner, adverb, noun'],
    'but': [22, 'Preposition, adverb, conjunction'],
    'his': [23, 'Possessive pronoun'],
    'by': [24, 'Preposition'],
    'from': [25, 'Preposition'],
    'they': [26, 'Pronoun'],
    'we': [27, 'Pronoun'],
    'say': [28, 'Verb et al.'],
    'her': [29, 'Possessive pronoun'],
    'she': [30, 'Pronoun'],
    'or': [31, 'Conjunction'],
    'an': [32, 'Article'],
    'will': [33, 'Verb, noun'],
    'my': [34, 'Possessive pronoun'],
    'one': [35, 'Noun, adjective, et al.'],
    'all': [36, 'Adjective'],
    'would': [37, 'Verb'],
    'there': [38, 'Adverb, pronoun, et al.'],
    'their': [39, 'Possessive pronoun'],
    'what': [40, 'Pronoun, adverb, et al.'],
    'so': [41, 'Conjunction, adverb, et al.'],
    'up': [42, 'Adverb, preposition, et al.'],
    'out': [43, 'Preposition'],
    'if': [44, 'Conjunction'],
    'about': [45, 'Preposition, adverb, et al.'],
    'who': [46, 'Pronoun, noun'],
    'get': [47, 'Verb'],
    'which': [48, 'Pronoun'],
    'go': [49, 'Verb, noun'],
    'me': [50, 'Pronoun'],
    'when': [51, 'Adverb'],
    'make': [52, 'Verb, noun'],
    'can': [53, 'Verb, noun'],
    'like': [54, 'Preposition, verb'],
    'time': [55, 'Noun'],
    'no': [56, 'Determiner, adverb'],
    'just': [57, 'Adjective'],
    'him': [58, 'Pronoun'],
    'know': [59, 'Verb, noun'],
    'take': [60, 'Verb, noun'],
    'people': [61, 'Noun'],
    'into': [62, 'Preposition'],
    'year': [63, 'Noun'],
    'your': [64, 'Possessive pronoun'],
    'good': [65, 'Adjective'],
    'some': [66, 'Determiner, pronoun'],
    'could': [67, 'Verb'],
    'them': [68, 'Pronoun'],
    'see': [69, 'Verb'],
    'other': [70, 'Adjective, pronoun'],
    'than': [71, 'Conjunction, preposition'],
    'then': [72, 'Adverb'],
    'now': [73, 'Preposition'],
    'look': [74, 'Verb'],
    'only': [75, 'Adverb'],
    'come': [76, 'Verb'],
    'its': [77, 'Possessive pronoun'],
    'over': [78, 'Preposition'],
    'think': [79, 'Verb'],
    'also': [80, 'Adverb'],
    'back': [81, 'Noun, adverb'],
    'after': [82, 'Preposition'],
    'use': [83, 'Verb, noun'],
    'two': [84, 'Noun'],
    'how': [85, 'Adverb'],
    'our': [86, 'Possessive pronoun'],
    'work': [87, 'Verb, noun'],
    'first': [88, 'Adjective'],
    'well': [89, 'Adverb'],
    'way': [90, 'Noun, adverb'],
    'even': [91, 'Adjective'],
    'new': [92, 'Adjective et al.'],
    'want': [93, 'Verb'],
    'because': [94, 'Conjunction'],
    'any': [95, 'Pronoun'],
    'these': [96, 'Pronoun'],
    'give': [97, 'Verb'],
    'day': [98, 'Noun'],
    'most': [99, 'Adverb'],
    'us': [100, 'Pronoun']}

# from https://simple.wikipedia.org/wiki/Wikipedia:List_of_1000_basic_words
# 998 (from 1000_basic_words) - 90 (from 100 Most_common_words) + 1 ('tears') = 909 words
from100_to1000_basic_words = [
    'above',
    'across',
    'act',
    'active',
    'activity',
    'add',
    'afraid',
    'again',
    'age',
    'ago',
    'agree',
    'air',
    'alone',
    'along',
    'already',
    'always',
    'am',
    'amount',
    'angry',
    'another',
    'answer',
    'anyone',
    'anything',
    'anytime',
    'appear',
    'apple',
    'are',
    'area',
    'arm',
    'army',
    'around',
    'arrive',
    'art',
    'ask',
    'attack',
    'aunt',
    'autumn',
    'away',
    'baby',
    'bad',
    'bag',
    'ball',
    'bank',
    'base',
    'basket',
    'bath',
    'bean',
    'bear',
    'beautiful',
    'bed',
    'bedroom',
    'beer',
    'behave',
    'before',
    'begin',
    'behind',
    'bell',
    'below',
    'besides',
    'best',
    'better',
    'between',
    'big',
    'bird',
    'birth',
    'birthday',
    'bit',
    'bite',
    'black',
    'bleed',
    'block',
    'blood',
    'blow',
    'blue',
    'board',
    'boat',
    'body',
    'boil',
    'bone',
    'book',
    'border',
    'born',
    'borrow',
    'both',
    'bottle',
    'bottom',
    'bowl',
    'box',
    'boy',
    'branch',
    'brave',
    'bread',
    'break',
    'breakfast',
    'breathe',
    'bridge',
    'bright',
    'bring',
    'brother',
    'brown',
    'brush',
    'build',
    'burn',
    'business',
    'bus',
    'busy',
    'buy',
    'cake',
    'call',
    'candle',
    'cap',
    'car',
    'card',
    'care',
    'careful',
    'careless',
    'carry',
    'case',
    'cat',
    'catch',
    'central',
    'century',
    'certain',
    'chair',
    'chance',
    'change',
    'chase',
    'cheap',
    'cheese',
    'chicken',
    'child',
    'children',
    'chocolate',
    'choice',
    'choose',
    'circle',
    'city',
    'class',
    'clever',
    'clean',
    'clear',
    'climb',
    'clock',
    'cloth',
    'clothes',
    'cloud',
    'cloudy',
    'close',
    'coffee',
    'coat',
    'coin',
    'cold',
    'collect',
    'colour',
    'comb',
    'comfortable',
    'common',
    'compare',
    'complete',
    'computer',
    'condition',
    'continue',
    'control',
    'cook',
    'cool',
    'copper',
    'corn',
    'corner',
    'correct',
    'cost',
    'contain',
    'count',
    'country',
    'course',
    'cover',
    'crash',
    'cross',
    'cry',
    'cup',
    'cupboard',
    'cut',
    'dance',
    'dangerous',
    'dark',
    'daughter',
    'dead',
    'decide',
    'decrease',
    'deep',
    'deer',
    'depend',
    'desk',
    'destroy',
    'develop',
    'die',
    'different',
    'difficult',
    'dinner',
    'direction',
    'dirty',
    'discover',
    'dish',
    'dog',
    'door',
    'double',
    'down',
    'draw',
    'dream',
    'dress',
    'drink',
    'drive',
    'drop',
    'dry',
    'duck',
    'dust',
    'duty',
    'each',
    'ear',
    'early',
    'earn',
    'earth',
    'east',
    'easy',
    'eat',
    'education',
    'effect',
    'egg',
    'eight',
    'either',
    'electric',
    'elephant',
    'else',
    'empty',
    'end',
    'enemy',
    'enjoy',
    'enough',
    'enter',
    'equal',
    'entrance',
    'escape',
    'evening',
    'event',
    'ever',
    'every',
    'everyone',
    'everybody',
    'exact',
    'examination',
    'example',
    'except',
    'excited',
    'exercise',
    'expect',
    'expensive',
    'explain',
    'extremely',
    'eye',
    'face',
    'fact',
    'fail',
    'fall',
    'false',
    'family',
    'famous',
    'far',
    'farm',
    'father',
    'fast',
    'fat',
    'fault',
    'fear',
    'feed',
    'feel',
    'female',
    'fever',
    'few',
    'fight',
    'fill',
    'film',
    'find',
    'fine',
    'finger',
    'finish',
    'fire',
    'fish',
    'fit',
    'five',
    'fix',
    'flag',
    'flat',
    'float',
    'floor',
    'flour',
    'flower',
    'fly',
    'fold',
    'food',
    'fool',
    'foot',
    'football',
    'force',
    'foreign',
    'forest',
    'forget',
    'forgive',
    'fork',
    'form',
    'fox',
    'four',
    'free',
    'freedom',
    'freeze',
    'fresh',
    'friend',
    'friendly',
    'front',
    'fruit',
    'full',
    'fun',
    'funny',
    'furniture',
    'further',
    'future',
    'game',
    'garden',
    'gate',
    'general',
    'gentleman',
    'gift',
    'glad',
    'glass',
    'goat',
    'god',
    'gold',
    'goodbye',
    'grandfather',
    'grandmother',
    'grass',
    'grave',
    'great',
    'green',
    'gray',
    'ground',
    'group',
    'grow',
    'gun',
    'hair',
    'half',
    'hall',
    'hammer',
    'hand',
    'happen',
    'happy',
    'hard',
    'hat',
    'hate',
    'head',
    'healthy',
    'hear',
    'heavy',
    'heart',
    'heaven',
    'height',
    'hello',
    'help',
    'hen',
    'here',
    'hers',
    'hide',
    'high',
    'hill',
    'hit',
    'hobby',
    'hold',
    'hole',
    'holiday',
    'home',
    'hope',
    'horse',
    'hospital',
    'hot',
    'hotel',
    'house',
    'hundred',
    'hungry',
    'hour',
    'hurry',
    'husband',
    'hurt',
    'ice',
    'idea',
    'important',
    'increase',
    'inside',
    'introduce',
    'invent',
    'iron',
    'invite',
    'is',
    'island',
    'jelly',
    'job',
    'join',
    'juice',
    'jump',
    'keep',
    'key',
    'kill',
    'kind',
    'king',
    'kitchen',
    'knee',
    'knife',
    'knock',
    'ladder',
    'lady',
    'lamp',
    'land',
    'large',
    'last',
    'late',
    'lately',
    'laugh',
    'lazy',
    'lead',
    'leaf',
    'learn',
    'leave',
    'leg',
    'left',
    'lend',
    'length',
    'less',
    'lesson',
    'let',
    'letter',
    'library',
    'lie',
    'life',
    'light',
    'lion',
    'lip',
    'list',
    'listen',
    'little',
    'live',
    'lock',
    'lonely',
    'long',
    'lose',
    'lot',
    'love',
    'low',
    'lower',
    'luck',
    'machine',
    'main',
    'male',
    'man',
    'many',
    'map',
    'mark',
    'market',
    'marry',
    'matter',
    'may',
    'meal',
    'mean',
    'measure',
    'meat',
    'medicine',
    'meet',
    'member',
    'mention',
    'method',
    'middle',
    'milk',
    'million',
    'mind',
    'minute',
    'miss',
    'mistake',
    'mix',
    'model',
    'modern',
    'moment',
    'money',
    'monkey',
    'month',
    'moon',
    'more',
    'morning',
    'mother',
    'mountain',
    'mouth',
    'move',
    'much',
    'music',
    'must',
    'name',
    'narrow',
    'nation',
    'nature',
    'near',
    'nearly',
    'neck',
    'need',
    'needle',
    'neighbour',
    'neither',
    'net',
    'never',
    'news',
    'newspaper',
    'next',
    'nice',
    'night',
    'nine',
    'noble',
    'noise',
    'none',
    'nor',
    'north',
    'nose',
    'nothing',
    'notice',
    'number',
    'obey',
    'object',
    'ocean',
    'off',
    'offer',
    'office',
    'often',
    'oil',
    'old',
    'open',
    'opposite',
    'orange',
    'order',
    'outside',
    'own',
    'page',
    'pain',
    'paint',
    'pair',
    'pan',
    'paper',
    'parent',
    'park',
    'part',
    'partner',
    'party',
    'pass',
    'past',
    'path',
    'pay',
    'peace',
    'pen',
    'pencil',
    'pepper',
    'per',
    'perfect',
    'period',
    'person',
    'petrol',
    'photograph',
    'piano',
    'pick',
    'picture',
    'piece',
    'pig',
    'pin',
    'pink',
    'place',
    'plane',
    'plant',
    'plastic',
    'plate',
    'play',
    'please',
    'pleased',
    'plenty',
    'pocket',
    'point',
    'poison',
    'police',
    'polite',
    'pool',
    'poor',
    'popular',
    'position',
    'possible',
    'potato',
    'pour',
    'power',
    'present',
    'press',
    'pretty',
    'prevent',
    'price',
    'prince',
    'prison',
    'private',
    'prize',
    'probably',
    'problem',
    'produce',
    'promise',
    'proper',
    'protect',
    'provide',
    'public',
    'pull',
    'punish',
    'pupil',
    'push',
    'put',
    'queen',
    'question',
    'quick',
    'quiet',
    'quite',
    'radio',
    'rain',
    'rainy',
    'raise',
    'reach',
    'read',
    'ready',
    'real',
    'really',
    'receive',
    'record',
    'red',
    'remember',
    'remind',
    'remove',
    'rent',
    'repair',
    'repeat',
    'reply',
    'report',
    'rest',
    'restaurant',
    'result',
    'return',
    'rice',
    'rich',
    'ride',
    'right',
    'ring',
    'rise',
    'road',
    'rob',
    'rock',
    'room',
    'round',
    'rubber',
    'rude',
    'rule',
    'ruler',
    'run',
    'rush',
    'sad',
    'safe',
    'sail',
    'salt',
    'same',
    'sand',
    'save',
    'school',
    'science',
    'scissors',
    'search',
    'seat',
    'second',
    'seem',
    'sell',
    'send',
    'sentence',
    'serve',
    'seven',
    'several',
    'sex',
    'shade',
    'shadow',
    'shake',
    'shape',
    'share',
    'sharp',
    'sheep',
    'sheet',
    'shelf',
    'shine',
    'ship',
    'shirt',
    'shoe',
    'shoot',
    'shop',
    'short',
    'should',
    'shoulder',
    'shout',
    'show',
    'sick',
    'side',
    'signal',
    'silence',
    'silly',
    'silver',
    'similar',
    'simple',
    'single',
    'since',
    'sing',
    'sink',
    'sister',
    'sit',
    'six',
    'size',
    'skill',
    'skin',
    'skirt',
    'sky',
    'sleep',
    'slip',
    'slow',
    'small',
    'smell',
    'smile',
    'smoke',
    'snow',
    'soap',
    'sock',
    'soft',
    'someone',
    'something',
    'sometimes',
    'son',
    'soon',
    'sorry',
    'sound',
    'soup',
    'south',
    'space',
    'speak',
    'special',
    'speed',
    'spell',
    'spend',
    'spoon',
    'sport',
    'spread',
    'spring',
    'square',
    'stamp',
    'stand',
    'star',
    'start',
    'station',
    'stay',
    'steal',
    'steam',
    'step',
    'still',
    'stomach',
    'stone',
    'stop',
    'store',
    'storm',
    'story',
    'strange',
    'street',
    'strong',
    'structure',
    'student',
    'study',
    'stupid',
    'subject',
    'substance',
    'successful',
    'such',
    'sudden',
    'sugar',
    'suitable',
    'summer',
    'sun',
    'sunny',
    'support',
    'sure',
    'surprise',
    'sweet',
    'swim',
    'sword',
    'table',
    'talk',
    'tall',
    'taste',
    'taxi',
    'tea',
    'teach',
    'team',
    'tear',
    'tears',
    'telephone',
    'television',
    'tell',
    'ten',
    'tennis',
    'terrible',
    'test',
    'therefore',
    'thick',
    'thin',
    'thing',
    'third',
    'though',
    'threat',
    'three',
    'tidy',
    'tie',
    'title',
    'today',
    'toe',
    'together',
    'tomorrow',
    'tonight',
    'too',
    'tool',
    'tooth',
    'top',
    'total',
    'touch',
    'town',
    'train',
    'tram',
    'travel',
    'tree',
    'trouble',
    'true',
    'trust',
    'twice',
    'try',
    'turn',
    'type',
    'ugly',
    'uncle',
    'under',
    'understand',
    'unit',
    'until',
    'useful',
    'usual',
    'usually',
    'vegetable',
    'very',
    'village',
    'voice',
    'visit',
    'wait',
    'wake',
    'walk',
    'warm',
    'was',
    'wash',
    'waste',
    'watch',
    'water',
    'weak',
    'wear',
    'weather',
    'wedding',
    'week',
    'weight',
    'welcome',
    'were',
    'west',
    'wet',
    'wheel',
    'where',
    'while',
    'white',
    'why',
    'wide',
    'wife',
    'wild',
    'win',
    'wind',
    'window',
    'wine',
    'winter',
    'wire',
    'wise',
    'wish',
    'without',
    'woman',
    'wonder',
    'word',
    'world',
    'worry',
    'yard',
    'yell',
    'yesterday',
    'yet',
    'young',
    'zero',
    'zoo'
]