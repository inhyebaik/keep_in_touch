# -*- coding: utf-8 -*-
import sys
reload(sys)  
sys.setdefaultencoding('Cp1252')
import random

QUOTES = {
            "Christopher Moore (The Stupidest Angel, A Heartwarming Tale of Christmas Terror": "Christmas Amnesty. You can fall out of contact with a friend, fail to return calls, ignore e-mails, avoid eye contact at the Thrifty-Mart, forget birthdays, anniversaries, and reunions, and if you show up at their house during the holidays (with a gift) they are socially bound to forgive you -- act like nothing happened. Decorum dictates that the friendship move forward from that point, without guilt or recrimination. If you started a chess game ten years ago in October, you need only remember whose move it is -- or why you sold the chessboard and bought an Xbox in the interim. (Look, Christmas Amnesty is a wonderful thing, but it's not a dimensional shift. The laws of time and space continue to apply, even if you have been avoiding your friends. But don't try using the expansion of the universe an as excuse -- like you kept meaning to stop by, but their house kept getting farther away. That crap won't wash. Just say, 'Sorry I haven't called. Merry Christmas' Then show the present. Christmas Amnesty protocol dictates that your friend say, 'That's okay,' and let you in without further comment. This is the way it has always been done.",    
            "J.K. Rowling (Harry Potter and the Prisoner of Azkaban)": "He was my mum and dad's best friend. He's a convicted murderer, but he's broken out of wizard prison and he's on the run. He likes to keep in touch with me, though...keep up with my news...check if I'm happy...", 
            "David Levithan (How They Met, and Other Stories)": "We'd said we'd keep in touch. But touch is not something you can keep; as soon as it's gone, it's gone. We should have said we'd keep in words, because they are all we can string between us--words on a telephone line, words appearing on a screen." , 
            "Nicholas Sparks (The Notebook)": "But in every boy I met in the next few years, I found myself looking for you, and when the feelings got too strong, I'd write you another letter.", 
            "Lemony Snicket (The Beatrice Letters)":"Strange as it may seem, I still hope for the best, even though the best, like an interesting piece of mail, so rarely arrives, and even when it does it can be lost so easily.", 
            "J.K. Rowling (Harry Potter and the Sorcerer's Stone)": "One small hand closed on the letter beside him and he slept on, not knowing he was special, not knowing he was famous, not knowing he would be woken in a few hours' time by Mrs. Dursley's scream as she opened the front door to put out the milk bottles, nor that he would spend the next few weeks being prodded and pinched by his cousin Dudley...He couldn't know that at this very moment, people meeting in secret all over the country were holding up their glasses and saying in hushed voices, 'To Harry Potter - the boy who lived!'",
            "Mark Twain": "I didn't have time to write a short letter, so I wrote a long one instead.", 
            "Neil Gaiman": "Let us begin this letter, this prelude to an encounter, formally, as a declaration, in the old-fashioned way, I love you. You do not know me (although you have seen me, smiled at me). I know you (although not so well as I would like. I want to be there when your eyes flutter open in the morning, and you see me, and you smile. Surely this would be paradise enough?). So I do declare myself to you now, with pen set to paper. I declare it again, I love you.", 
            "C.S. Lewis": "Miracles are a retelling in small letters of the very same story which is written across the whole world in letters too large for some of us to see.", 
            "Mary Schmich (Wear Sunscreen, A Primer for Real Life)": "Keep your old love letters. Throw away your old bank statements.", 
            "Franz Kafka (Letter to Max Brod, July 5, 1922)": "A non-writing writer is a monster courting insanity.", 
            "J.K. Rowling (Harry Potter and the Prisoner of Azkaban)": "'What's that?' he snarled, staring at the envelope Harry was still clutching in his hand. 'If it's another form for me to sign, you've got another -' 'It\'s not,' said Harry cheerfully. 'It's a letter from my godfather.'", 
            "Mother Theresa": "God made the world for the delight of human beings--if we could see His goodness everywhere, His concern for us, His awareness of our needs, the phone call we've waited for, the ride we are offered, the letter in the mail, just the little things He does for us throughout the day.", 
            "Blaise Pascal (The Provincial Letters)": "I have only made this letter longer because I have not had the time to make it shorter.", 
            "Lemony Snicket (The Beatrice Letters)":"Strange as it may seem, I still hope for the best, even though the best, like an interesting piece of mail, so rarely arrives, and even when it does it can be lost so easily.",
            "Harriet Beecher Stowe (Uncle Tom's Cabin)":"He returned south to make arrangements for their marriage, when, most unexpectedly, his letters were returned to him by mail, with a short note from her guardian, stating to him that ere this reached him the lady would be the wife of another.",
            "Naomi Shihab Nye (Words Under the Words, Selected Poems)":"Then it is only kindness that makes sense anymore, only kindness that ties your shoes and sends you out into the day to mail letters and purchase bread, only kindness that raises its head from the crowd of the world to say It is I you have been looking for, and then goes with you everywhere like a shadow or a friend.", 
            "Cecelia Ahern (Love, Rosie)":"All I get is a quick text or a rushed e-mail from you every few days. I know you are busy and I know you have Bethany, but hello? I'm supposed to be your best friend.",
            "Nora Ephron (You've Got Mail)":"So much of what I see reminds me of something I read in a book, when shouldn't it be the other way around? I don't really want an answer. I just want to send this cosmic question out into the void. So good night, dear void.",
            "Daria Snadowsky (Anatomy of a Boyfriend (Anatomy, #1))":"I'll never be able to check my e-mail without praying I'll find a message from you with the subject line I love you, Dom - please come back to me.",
            "Scott Douglas (Quiet, Please, Dispatches From A Public Librarian)":"I am convinced that grandkids are inherently evil people who tell their grandparents to 'just go to the library and open up an e-mail account - it's free and so simple.'", 
            "Thomas de Quincey (Confessions of an English Opium Eater)":"Here was the secret of happiness, about which philosophers had disputed for so many ages, at once discovered; happiness might now be bought for a penny, and carried in the waistcoat-pocket; portable ecstasies might be had corked up in a pint-bottle; and peace of mind could be sent down by the mail." 
         }

def random_quote(QUOTES): 
    """returns random quote."""
    q = random.choice(QUOTES.items())
    author, quote = q
    return q


messages = {
            "hb":   [
                        "May this day bring to you all things that make you smile.", 
                        "Age is just a value; the higher the age the higher its value.", 
                        "Your birthday only comes around once a year so let's make today a day to remember.", 
                        "May every glowing candle on your cake transorm into a wish that will turn into reality.", 
                        "Because you're you, I'm celebrating today! Happy Birthday.", 
                        "May this year be your best ever.", 
                        "A birthday is just the first day of another 365-day journey around the sun. Enjoy the trip.", 
                        "Smile! It's your birthday.", 
                        "Here's to another year of experience.", 
                        "Have a wonderful day and fabulous year.", 
                        "You may grow a year old every year, but I hope your spirit remains fresh and youthful. Happy Birthday!", 
                        "You're aged to perfection. Happy birthday!", 
                        "My biggest Birthday wish for you is that you should stay the way you are. Don't ever change. Many happy returns of the day!", 
                        "If there was a book called 101 ways to be a great person, I would dedicate it to you! May all your Birthdays make you a better than what you already are!", 
                        "Happy birthday, may this day always be a special one to remember.", 
                        "You've got everything it takes to be successful. This Birthday, make yourself a promise that you will achieve your goals and dreams in life, no matter what. Wishing you a very Happy Birthday.", 
                        "Hope your birthday is just the beginning of a year full of happiness.", 
                        "I sealed my Birthday wishes for you in an envelope full of love and respect so that it reaches you and goes straight to your heart. Have a wonderful year ahead.", 
                        "Happy Birthday and many happy returns of the day.", 
                        "You'll never again be as young as you are today, so have fun and enjoy your day.", 
                        "Have you been moonlighting in my life as my pillar of strength and support while you're actually an angel sent from the heavens? You're too good to be true! I wish you a very Happy Birthday.", 
                        "Happy birthday, may this day always be a special one to remember.", 
                        "May Time, Lady Luck and Mistress Fortune always be on your side. Once they are, nothing in the world will be able to stop you. Have a great Birthday!", 
                        "Birthdays Mean: cake, presents, wrapping paper, money, clothes, friends, partys etc. What more could you want on your birthday?"
                    ],


            "ty" :  [
                        "You're the best.", 
                        "I'm humbled and grateful.", 
                        "You knocked me off my feet!", 
                        "My heart is still smiling.", 
                        "Your thoughtfulness is a gift I will always treasure.", 
                        "Sometimes the simplest things mean the most.", 
                        "The banana bread was fabulous. You made my day.", 
                        "I'm touched beyond words.", 
                        "All I can say is wow! (Except, of course, I'm grateful.)", 
                        "My heart just keeps thanking you and thanking you.", 
                        "You're a blessing to me.", 
                        "Thank you for being my angel.", 
                        "This has been a challenging time, and I appreciate you so much.", 
                        "You have no idea how much your help has meant.", 
                        "For all the little and big ways you've pitched in…thanks!", 
                        "There was nothing random about your acts of kindness. Thank you for all you have done.", 
                        "I can never thank you enough. But this is a start.", 
                        "You always know how to make life brighter for everyone you know.", 
                        "I can't possibly repay you.", 
                        "You are always so helpful.", 
                        "You make the world a nicer place.", 
                        "You went above and beyond, and I am touched and grateful.", 
                        "You took common courtesy to an uncommon level. We're so grateful for your help."
                    ],

            "fup":  [
                        "Thank you so much for inviting me to interview for your open account specialist position. I truly appreciate the time you took to talk with me about this opportunity and the company. I enjoyed learning more about your work group and how I might fit into that team. Please don't hesitate to contact me with any follow-up questions you might have. I hope to talk with you again soon.", 
                        "Thank you for your invaluable mentoring these past three months. I've had fun getting to know you better, and I've learned so much from talking with you and seeing how you work. You are amazing at what you do! I'm grateful to have had the chance to work with you so closely.", 
                        "I can't thank you enough for advising me to send my résumé to your colleague. I now have an interview scheduled with her next week to discuss some freelance work, and I'm really excited about the assignment she's describing. It was very kind of you to refer me to her. I hope I can find a way to return the favor soon!"
                    ],
          }

def random_message(template_type):
    """returns random message"""
    i = random.randint(0, len(messages[template_type])-1)
    return messages[template_type][i]


