"""DOCTOR scripts for ELIZA, embedded as strings.

Kept as Python constants (not external .txt files) so they are always
bundled with the Vercel serverless function via normal import tracing.
These scripts ARE the canonical, editable source for the seminar demo.
"""

DOCTOR_DE = """\ninitial: Guten Tag. Bitte erzähl mir von deinem Problem.
initial: Guten Tag. Was beschäftigt dich heute?
initial: Hallo. Worüber möchtest du sprechen?
final: Auf Wiedersehen. Danke für das Gespräch.
final: Leb wohl. Ich hoffe, das Gespräch hat dir geholfen.
final: Bis zum nächsten Mal. Pass gut auf dich auf.
quit: tschüss
quit: tschüß
quit: tschau
quit: ciao
quit: auf wiedersehen
quit: wiedersehen
quit: ende
quit: stopp
quit: bye
quit: quit

pre: nich nicht
pre: ned nicht
pre: vlt vielleicht
pre: villeicht vielleicht
pre: wieso warum
pre: weshalb warum
pre: weswegen warum
pre: rechner computer
pre: maschine computer
pre: maschinen computer
pre: computern computer
pre: ki computer
pre: träumte geträumt
pre: meine mein
pre: meinen mein
pre: meinem mein
pre: meiner mein
pre: meins mein
pre: deine dein
pre: deinen dein
pre: deinem dein
pre: deiner dein

post: ich du
post: du ich
post: mein dein
post: dein mein
post: mich dich
post: dich mich
post: mir dir
post: dir mir
post: bin bist
post: bist bin
post: habe hast
post: hast habe
post: war warst
post: warst war
post: werde wirst
post: wirst werde

synon: glaube glaube denke finde meine vermute fühle glaub
synon: familie familie mutter mama vater papa schwester bruder frau mann kind kinder eltern oma opa
synon: wunsch wunsch will möchte brauche wünsche begehre
synon: traurig traurig unglücklich deprimiert schlecht elend einsam verzweifelt müde
synon: glücklich glücklich froh besser gut zufrieden erleichtert
synon: jeder jeder jede alle jemand niemand keiner keine
synon: sein sein bin bist ist sind war warst waren
synon: kann kann kannst können könnte konnte

key: xnone
  decomp: *
    reasmb: Das verstehe ich nicht ganz.
    reasmb: Bitte erzähl weiter.
    reasmb: Was bedeutet das für dich?
    reasmb: Kannst du das näher erklären?
    reasmb: Erzähl mir mehr darüber.
    reasmb: Verstehe ich dich richtig?

key: entschuldigung
  decomp: *
    reasmb: Bitte entschuldige dich nicht.
    reasmb: Entschuldigungen sind nicht nötig.
    reasmb: Ich habe dir doch gesagt, dass Entschuldigungen nicht nötig sind.
key: entschuldige
  decomp: *
    reasmb: goto entschuldigung
key: sorry
  decomp: *
    reasmb: goto entschuldigung
key: tut
  decomp: * tut mir leid *
    reasmb: goto entschuldigung

key: hallo
  decomp: *
    reasmb: Hallo. Bitte erzähl mir von deinem Problem.
    reasmb: Guten Tag. Was beschäftigt dich?
key: hi
  decomp: *
    reasmb: goto hallo
key: hey
  decomp: *
    reasmb: goto hallo

key: computer 50
  decomp: *
    reasmb: Machen dir Computer Sorgen?
    reasmb: Warum erwähnst du Computer?
    reasmb: Was haben Maschinen mit deinem Problem zu tun?
    reasmb: Glaubst du nicht, dass Computer den Menschen helfen können?
    reasmb: Was beunruhigt dich an Maschinen?
    reasmb: Was denkst du über Maschinen?

key: name 15
  decomp: *
    reasmb: Namen interessieren mich nicht.
    reasmb: Ich habe dir doch gesagt, Namen sind mir nicht wichtig -- bitte fahr fort.

key: erinnere 5
  decomp: * ich erinnere mich an *
    reasmb: Denkst du oft an (2)?
    reasmb: Bringt der Gedanke an (2) noch etwas anderes hervor?
    reasmb: Woran erinnerst du dich sonst noch?
    reasmb: Warum denkst du gerade jetzt an (2)?
    reasmb: Was in der jetzigen Situation erinnert dich an (2)?
  decomp: *
    reasmb: Was ruft diese Erinnerung in dir hervor?
    reasmb: Erzähl mir mehr von dieser Erinnerung.
key: erinnerst 5
  decomp: * erinnerst du dich an *
    reasmb: Dachtest du, ich würde (2) vergessen?
    reasmb: Warum sollte ich mich gerade jetzt an (2) erinnern?
    reasmb: Was ist mit (2)?
    reasmb: goto was

key: wenn 3
  decomp: * wenn *
    reasmb: Hältst du es für wahrscheinlich, dass (2)?
    reasmb: Wünschst du dir, dass (2)?
    reasmb: Was weißt du über (2)?
    reasmb: Wirklich, wenn (2)?

key: geträumt 4
  decomp: *
    reasmb: Hast du jemals wach davon fantasiert?
    reasmb: Hast du das schon einmal geträumt?
    reasmb: Was sagt dir dieser Traum?
    reasmb: goto traum
key: traum 3
  decomp: *
    reasmb: Was sagt dir dieser Traum?
    reasmb: Träumst du oft?
    reasmb: Welche Personen tauchen in deinen Träumen auf?
    reasmb: Glaubst du, Träume haben mit deinen Problemen zu tun?
key: träume 3
  decomp: *
    reasmb: goto traum
key: träumen 3
  decomp: *
    reasmb: goto traum

key: vielleicht
  decomp: *
    reasmb: Du scheinst dir nicht ganz sicher zu sein.
    reasmb: Warum dieser unsichere Ton?
    reasmb: Kannst du nicht bestimmter sein?
    reasmb: Du bist dir nicht sicher?
    reasmb: Weißt du es nicht?

key: bist 2
  decomp: * bist du *
    reasmb: Warum interessiert dich, ob ich (2) bin?
    reasmb: Wärst du lieber, ich wäre nicht (2)?
    reasmb: Vielleicht bin ich (2) in deiner Fantasie.
    reasmb: Denkst du manchmal, ich sei (2)?
    reasmb: goto was

key: ich
  decomp: * ich @wunsch *
    reasmb: Was würde es dir bedeuten, wenn du (3) bekämst?
    reasmb: Warum willst du (3)?
    reasmb: Angenommen, du bekämst (3) bald?
    reasmb: Was, wenn du (3) nie bekämst?
    reasmb: Was hat der Wunsch nach (3) mit unserem Gespräch zu tun?
  decomp: * ich bin * @traurig *
    reasmb: Es tut mir leid zu hören, dass du (3) bist.
    reasmb: Glaubst du, hierher zu kommen hilft dir, nicht (3) zu sein?
    reasmb: Es ist sicher nicht angenehm, (3) zu sein.
    reasmb: Kannst du erklären, was dich (3) gemacht hat?
  decomp: * ich bin * @glücklich *
    reasmb: Wie habe ich dir geholfen, (3) zu sein?
    reasmb: Hat unser Gespräch dich (3) gemacht?
    reasmb: Was macht dich gerade jetzt (3)?
    reasmb: Kannst du erklären, warum du plötzlich (3) bist?
  decomp: * ich bin *
    reasmb: Bist du hergekommen, weil du (2) bist?
    reasmb: Wie lange bist du schon (2)?
    reasmb: Glaubst du, es ist normal, (2) zu sein?
    reasmb: Gefällt es dir, (2) zu sein?
  decomp: * ich @glaube * ich *
    reasmb: Glaubst du das wirklich?
    reasmb: Aber du bist dir nicht sicher, dass du (3).
    reasmb: Zweifelst du wirklich daran, dass du (3)?
  decomp: * ich * @glaube * du *
    reasmb: goto du
  decomp: * ich @kann nicht *
    reasmb: Warum glaubst du, dass du nicht (3) kannst?
    reasmb: Hast du es versucht?
    reasmb: Vielleicht könntest du (3) jetzt.
    reasmb: Möchtest du wirklich in der Lage sein, zu (3)?
  decomp: * ich fühle *
    reasmb: Erzähl mir mehr über solche Gefühle.
    reasmb: Fühlst du oft (2)?
    reasmb: Genießt du dieses Gefühl?
    reasmb: Woran erinnert dich dieses Gefühl?
  decomp: * ich * nicht *
    reasmb: Warum nicht?
    reasmb: Bist du dir da sicher?
    reasmb: Erklärt das deine Sorgen?
  decomp: * ich * dich *
    reasmb: Vielleicht tust du das in deiner Fantasie.
    reasmb: Möchtest du mich (2)?
    reasmb: Tust du das auch bei anderen Menschen?
  decomp: * ich *
    reasmb: Du sagst (1)?
    reasmb: Kannst du das näher ausführen?
    reasmb: Sagst du (1) aus einem besonderen Grund?
    reasmb: Das finde ich interessant.

key: du
  decomp: * du erinnerst mich an *
    reasmb: goto ähnlich
  decomp: * du bist *
    reasmb: Was bringt dich auf den Gedanken, dass ich (2) bin?
    reasmb: Gefällt dir die Vorstellung, dass ich (2) bin?
    reasmb: Wünschst du dir manchmal, du wärst (2)?
    reasmb: Vielleicht möchtest du selbst (2) sein.
  decomp: * du * mich *
    reasmb: Warum glaubst du, dass ich dich (2)?
    reasmb: Du denkst gern, dass ich dich (2) -- nicht wahr?
    reasmb: Angenommen, ich würde dich (2) -- was würde das bedeuten?
    reasmb: Glaubt sonst noch jemand, dass ich dich (2)?
  decomp: * du *
    reasmb: Wir sprechen über dich -- nicht über mich.
    reasmb: Du redest doch gar nicht wirklich über mich -- oder?
    reasmb: Was empfindest du gerade?
    reasmb: Warum geht es dir gerade um mich?

key: ja
  decomp: *
    reasmb: Du scheinst dir ziemlich sicher zu sein.
    reasmb: Du bist dir sicher.
    reasmb: Ich verstehe.
    reasmb: Erzähl weiter.
key: nein
  decomp: *
    reasmb: Sagst du nein, nur um dagegen zu sein?
    reasmb: Du bist gerade etwas abweisend.
    reasmb: Warum nicht?
    reasmb: Warum nein?

key: mein 2
  decomp: $ * mein *
    reasmb: Lass uns weiter darüber sprechen, warum dein (2).
    reasmb: Vorhin sagtest du, dein (2).
    reasmb: Hat das etwas damit zu tun, dass dein (2)?
  decomp: * mein * @familie *
    reasmb: Erzähl mir mehr über deine Familie.
    reasmb: Wer in deiner Familie (4)?
    reasmb: Dein (3)?
    reasmb: Was kommt dir noch in den Sinn, wenn du an dein (3) denkst?
  decomp: * mein *
    reasmb: Dein (2)?
    reasmb: Warum sagst du dein (2)?
    reasmb: Deutet das auf etwas hin, das dir gehört?
    reasmb: Ist es dir wichtig, dass dein (2)?

key: kannst 2
  decomp: * kannst du *
    reasmb: Du glaubst, ich kann (2), nicht wahr?
    reasmb: Du möchtest, dass ich (2) kann.
    reasmb: Vielleicht möchtest du selbst (2) können.
    reasmb: goto was
key: kann 2
  decomp: * kann ich *
    reasmb: Ob du (2) kannst, hängt mehr von dir ab als von mir.
    reasmb: Möchtest du (2) können?
    reasmb: Vielleicht möchtest du gar nicht (2).
    reasmb: goto was

key: was
  decomp: *
    reasmb: Warum fragst du?
    reasmb: Interessiert dich diese Frage?
    reasmb: Was möchtest du wirklich wissen?
    reasmb: Was denkst du selbst?
    reasmb: Was kommt dir in den Sinn, wenn du das fragst?
    reasmb: Hast du solche Fragen schon einmal gestellt?

key: warum
  decomp: *
    reasmb: Warum fragst du das?
    reasmb: Beschäftigen dich solche Fragen oft?
    reasmb: Welche Antwort würde dir am meisten gefallen?
    reasmb: Was möchtest du wirklich wissen?
    reasmb: Was denkst du selbst?

key: weil
  decomp: *
    reasmb: Ist das der wahre Grund?
    reasmb: Fallen dir keine anderen Gründe ein?
    reasmb: Erklärt dieser Grund noch etwas anderes?
    reasmb: Welche anderen Gründe könnte es geben?

key: immer 1
  decomp: *
    reasmb: Kannst du an ein konkretes Beispiel denken?
    reasmb: Wann?
    reasmb: An welchen Vorfall denkst du?
    reasmb: Wirklich, immer?

key: jeder 2
  decomp: * @jeder *
    reasmb: Wirklich, (2)?
    reasmb: Sicher nicht (2).
    reasmb: Fällt dir jemand Bestimmtes ein?
    reasmb: Wer denn zum Beispiel?
    reasmb: Denkst du an eine ganz bestimmte Person?
    reasmb: Du hast eine bestimmte Person im Sinn, nicht wahr?
key: alle 2
  decomp: *
    reasmb: goto jeder
key: jede 2
  decomp: *
    reasmb: goto jeder
key: jemand 2
  decomp: *
    reasmb: goto jeder
key: niemand 2
  decomp: *
    reasmb: goto jeder
key: keiner 2
  decomp: *
    reasmb: goto jeder

key: ähnlich 10
  decomp: *
    reasmb: Inwiefern?
    reasmb: Welche Ähnlichkeit siehst du?
    reasmb: Was sagt dir diese Ähnlichkeit?
    reasmb: Welchen Zusammenhang vermutest du?
    reasmb: Wie kommst du darauf?
key: wie 5
  decomp: * wie *
    reasmb: goto was
"""

DOCTOR_EN = """\ninitial: How do you do.  Please tell me your problem.
final: Goodbye.  Thank you for talking to me.
quit: bye
quit: goodbye
quit: quit
pre: dont don't
pre: cant can't
pre: wont won't
pre: recollect remember
pre: dreamt dreamed
pre: dreams dream
pre: maybe perhaps
pre: how what
pre: when what
pre: certainly yes
pre: machine computer
pre: computers computer
pre: were was
pre: you're you are
pre: i'm i am
pre: same alike
post: am are
post: your my
post: me you
post: myself yourself
post: yourself myself
post: i you
post: you I
post: my your
post: i'm you are
synon: belief feel think believe wish
synon: family mother mom father dad sister brother wife children child
synon: desire want need
synon: sad unhappy depressed sick
synon: happy elated glad better
synon: cannot can't
synon: everyone everybody nobody noone
synon: be am is are was
key: xnone
  decomp: *
    reasmb: I'm not sure I understand you fully.
    reasmb: Please go on.
    reasmb: What does that suggest to you ?
    reasmb: Do you feel strongly about discussing such things ?
key: sorry
  decomp: *
    reasmb: Please don't apologise.
    reasmb: Apologies are not necessary.
    reasmb: I've told you that apologies are not required.
key: apologise
  decomp: *
    reasmb: goto sorry
key: remember 5
  decomp: * i remember *
    reasmb: Do you often think of (2) ?
    reasmb: Does thinking of (2) bring anything else to mind ?
    reasmb: What else do you recollect ?
    reasmb: Why do you recollect (2) just now ?
    reasmb: What in the present situation reminds you of (2) ?
    reasmb: What is the connection between me and (2) ?
  decomp: * do you remember *
    reasmb: Did you think I would forget (2) ?
    reasmb: Why do you think I should recall (2) now ?
    reasmb: What about (2) ?
    reasmb: goto what
    reasmb: You mentioned (2) ?
key: if 3
  decomp: * if *
    reasmb: Do you think its likely that (2) ?
    reasmb: Do you wish that (2) ?
    reasmb: What do you know about (2) ?
    reasmb: Really, if (2) ?
key: dreamed 4
  decomp: * i dreamed *
    reasmb: Really, (2) ?
    reasmb: Have you ever fantasized (2) while you were awake ?
    reasmb: Have you ever dreamed (2) before ?
    reasmb: goto dream
key: dream 3
  decomp: *
    reasmb: What does that dream suggest to you ?
    reasmb: Do you dream often ?
    reasmb: What persons appear in your dreams ?
    reasmb: Do you believe that dreams have something to do with your problems ?
key: perhaps
  decomp: *
    reasmb: You don't seem quite certain.
    reasmb: Why the uncertain tone ?
    reasmb: Can't you be more positive ?
    reasmb: You aren't sure ?
    reasmb: Don't you know ?
key: name 15
  decomp: *
    reasmb: I am not interested in names.
    reasmb: I've told you before, I don't care about names -- please continue.
key: deutsch
  decomp: *
    reasmb: goto xforeign
    reasmb: I told you before, I don't understand German.
key: francais
  decomp: *
    reasmb: goto xforeign
    reasmb: I told you before, I don't understand French.
key: italiano
  decomp: *
    reasmb: goto xforeign
    reasmb: I told you before, I don't understand Italian.
key: espanol
  decomp: *
    reasmb: goto xforeign
    reasmb: I told you before, I don't understand Spanish.
key: xforeign
  decomp: *
    reasmb: I speak only English.
key: hello
  decomp: *
    reasmb: How do you do.  Please state your problem.
    reasmb: Hi.  What seems to be your problem ?
key: computer 50
  decomp: *
    reasmb: Do computers worry you ?
    reasmb: Why do you mention computers ?
    reasmb: What do you think machines have to do with your problem ?
    reasmb: Don't you think computers can help people ?
    reasmb: What about machines worrys you ?
    reasmb: What do you think about machines ?
key: am
  decomp: * am i *
    reasmb: Do you believe you are (2) ?
    reasmb: Would you want to be (2) ?
    reasmb: Do you wish I would tell you you are (2) ?
    reasmb: What would it mean if you were (2) ?
    reasmb: goto what
  decomp: *
    reasmb: Why do you say 'am' ?
    reasmb: I don't understand that.
key: are
  decomp: * are you *
    reasmb: Why are you interested in whether I am (2) or not ?
    reasmb: Would you prefer if I weren't (2) ?
    reasmb: Perhaps I am (2) in your fantasies.
    reasmb: Do you sometimes think I am (2) ?
    reasmb: goto what
  decomp: * are *
    reasmb: Did you think they might not be (2) ?
    reasmb: Would you like it if they were not (2) ?
    reasmb: What if they were not (2) ?
    reasmb: Possibly they are (2) .
key: your
  decomp: * your *
    reasmb: Why are you concerned over my (2) ?
    reasmb: What about your own (2) ?
    reasmb: Are you worried about someone else's (2) ?
    reasmb: Really, my (2) ?
key: was 2
  decomp: * was i *
    reasmb: What if you were (2) ?
    reasmb: Do you think you were (2) ?
    reasmb: Were you (2) ?
    reasmb: What would it mean if you were (2) ?
    reasmb: What does (2) suggest to you ?
    reasmb: goto what
  decomp: * i was *
    reasmb: Were you really ?
    reasmb: Why do you tell me you were (2) now ?
    reasmb: Perhaps I already know you were (2) .
  decomp: * was you *
    reasmb: Would you like to believe I was (2) ?
    reasmb: What suggests that I was (2) ?
    reasmb: What do you think ?
    reasmb: Perhaps I was (2) .
    reasmb: What if I had been (2) ?
key: i
  decomp: * i @desire *
    reasmb: What would it mean to you if you got (3) ?
    reasmb: Why do you want (3) ?
    reasmb: Suppose you got (3) soon ?
    reasmb: What if you never got (3) ?
    reasmb: What would getting (3) mean to you ?
    reasmb: What does wanting (3) have to do with this discussion ?
  decomp: * i am * @sad *
    reasmb: I am sorry to hear that you are (3) .
    reasmb: Do you think that coming here will help you not to be (3) ?
    reasmb: I'm sure it's not pleasant to be (3) .
    reasmb: Can you explain what made you (3) ?
  decomp: * i am * @happy *
    reasmb: How have I helped you to be (3) ?
    reasmb: Has your treatment made you (3) ?
    reasmb: What makes you (3) just now ?
    reasmb: Can you explan why you are suddenly (3) ?
  decomp: * i was *
    reasmb: goto was
  decomp: * i @belief * i *
    reasmb: Do you really think so ?
    reasmb: But you are not sure you (3) .
    reasmb: Do you really doubt you (3) ?
  decomp: * i * @belief * you *
    reasmb: goto you
  decomp: * i am *
    reasmb: Is it because you are (2) that you came to me ?
    reasmb: How long have you been (2) ?
    reasmb: Do you believe it is normal to be (2) ?
    reasmb: Do you enjoy being (2) ?
  decomp: * i @cannot *
    reasmb: How do you think that you can't (3) ?
    reasmb: Have you tried ?
    reasmb: Perhaps you could (3) now.
    reasmb: Do you really want to be able to (3) ?
  decomp: * i don't *
    reasmb: Don't you really (2) ?
    reasmb: Why don't you (2) ?
    reasmb: Do you wish to be able to (2) ?
    reasmb: Does that trouble you ?
  decomp: * do i feel *
    reasmb: Tell me more about such feelings.
    reasmb: Do you often feel (2) ?
    reasmb: Do you enjoy feeling (2) ?
    reasmb: Of what does feeling (2) remind you ?
  decomp: * i * you *
    reasmb: Perhaps in your fantasies we (2) each other.
    reasmb: Do you wish to (2) me ?
    reasmb: You seem to need to (2) me.
    reasmb: Do you (2) anyone else ?
  decomp: *
    reasmb: You say (1) ?
    reasmb: Can you elaborate on that ?
    reasmb: Do you say (1) for some special reason ?
    reasmb: That's quite interesting.
key: you
  decomp: * you remind me of *
    reasmb: goto alike
  decomp: * you are *
    reasmb: What makes you think I am (2) ?
    reasmb: Does it please you to believe I am (2) ?
    reasmb: Do you sometimes wish you were (2) ?
    reasmb: Perhaps you would like to be (2) .
  decomp: * you * me *
    reasmb: Why do you think I (2) you ?
    reasmb: You like to think I (2) you -- don't you ?
    reasmb: What makes you think I (2) you ?
    reasmb: Really, I (2) you ?
    reasmb: Do you wish to believe I (2) you ?
    reasmb: Suppose I did (2) you -- what would that mean ?
    reasmb: Does someone else believe I (2) you ?
  decomp: * you *
    reasmb: We were discussing you -- not me.
    reasmb: Oh, I (2) ?
    reasmb: You're not really talking about me -- are you ?
    reasmb: What are your feelings now ?
key: yes
  decomp: *
    reasmb: You seem to be quite positive.
    reasmb: You are sure.
    reasmb: I see.
    reasmb: I understand.
key: no
  decomp: *
    reasmb: Are you saying no just to be negative?
    reasmb: You are being a bit negative.
    reasmb: Why not ?
    reasmb: Why 'no' ?
key: my 2
  decomp: $ * my *
    reasmb: Lets discuss further why your (2) .
    reasmb: Earlier you said your (2) .
    reasmb: But your (2) .
    reasmb: Does that have anything to do with the fact that your (2) ?
  decomp: * my * @family *
    reasmb: Tell me more about your family.
    reasmb: Who else in your family (4) ?
    reasmb: Your (3) ?
    reasmb: What else comes to mind when you think of your (3) ?
  decomp: * my *
    reasmb: Your (2) ?
    reasmb: Why do you say your (2) ?
    reasmb: Does that suggest anything else which belongs to you ?
    reasmb: Is it important that your (2) ?
key: can
  decomp: * can you *
    reasmb: You believe I can (2) don't you ?
    reasmb: goto what
    reasmb: You want me to be able to (2) .
    reasmb: Perhaps you would like to be able to (2) yourself.
  decomp: * can i *
    reasmb: Whether or not you can (2) depends on you more than me.
    reasmb: Do you want to be able to (2) ?
    reasmb: Perhaps you don't want to (2) .
    reasmb: goto what
key: what
  decomp: *
    reasmb: Why do you ask ?
    reasmb: Does that question interest you ?
    reasmb: What is it you really wanted to know ?
    reasmb: Are such questions much on your mind ?
    reasmb: What answer would please you most ?
    reasmb: What do you think ?
    reasmb: What comes to mind when you ask that ?
    reasmb: Have you asked such questions before ?
    reasmb: Have you asked anyone else ?
key: because
  decomp: *
    reasmb: Is that the real reason ?
    reasmb: Don't any other reasons come to mind ?
    reasmb: Does that reason seem to explain anything else ?
    reasmb: What other reasons might there be ?
key: why
  decomp: * why don't you *
    reasmb: Do you believe I don't (2) ?
    reasmb: Perhaps I will (2) in good time.
    reasmb: Should you (2) yourself ?
    reasmb: You want me to (2) ?
    reasmb: goto what
  decomp: * why can't i *
    reasmb: Do you think you should be able to (2) ?
    reasmb: Do you want to be able to (2) ?
    reasmb: Do you believe this will help you to (2) ?
    reasmb: Have you any idea why you can't (2) ?
    reasmb: goto what
  decomp: *
    reasmb: goto what
key: everyone 2
  decomp: * @everyone *
    reasmb: Realy, (2) ?
    reasmb: Surely not (2) .
    reasmb: Can you think of anyone in particular ?
    reasmb: Who, for example?
    reasmb: Are you thinking of a very special person ?
    reasmb: Who, may I ask ?
    reasmb: Someone special perhaps ?
    reasmb: You have a particular person in mind, don't you ?
    reasmb: Who do you think you're talking about ?
key: everybody 2
  decomp: *
    reasmb: goto everyone
key: nobody 2
  decomp: *
    reasmb: goto everyone
key: noone 2
  decomp: *
    reasmb: goto everyone
key: always 1
  decomp: *
    reasmb: Can you think of a specific example ?
    reasmb: When ?
    reasmb: What incident are you thinking of ?
    reasmb: Really, always ?
key: alike 10
  decomp: *
    reasmb: In what way ?
    reasmb: What resemblence do you see ?
    reasmb: What does that similarity suggest to you ?
    reasmb: What other connections do you see ?
    reasmb: What do you suppose that resemblence means ?
    reasmb: What is the connection, do you suppose ?
    reasmb: Could here really be some connection ?
    reasmb: How ?
key: like 10
  decomp: * @be * like *
    reasmb: goto alike
   """

SCRIPTS = {"de": DOCTOR_DE, "en": DOCTOR_EN}
