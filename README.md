SlicerDHub

Hlavní výhodou aplikace je, že umožňuje uživatelům Fusion 360 exportovat modely a následně je jednoduše odeslat do různých slicerů, které nejsou oficiálně podporovány.

Hlavní funkce

Uložení exportovaného modelu do zvolené složky

Spuštění sliceru s předáním exportovaného souboru

Jednoduché GUI s podporou dlaždic pro slicery

Možnost přidat a odebrat slicery přímo z aplikace

Automatické rozpoznánání ikon sliceru (z .exe souboru)

Podpora světlého, tmavého nebo systémového tématu

Režim "editace" pro správu dlaždic



Vyzkoušené slicery:

Bambu Studio

Orca Slicer

IdeaMaker

PrusaSlicer / Prusa Studio

(Postupně budou přidávány další)

Požadavky

Windows 10/11

Python 3.10+ (doporučeno 64bit)

Nainstalován balíček:

customtkinter

Pillow

pywin32

pyinstaller (pro kompilaci)

Instalace a spuštění

1. Stažni repozitáře

git clone https://github.com/HDaveSoft/slicerdhub.git
cd slicerdhub

2. Spuštění verze v Pythonu

python slicerdhub.py

3. Vytvoření spustitelného .exe (volitelné)

build.bat

Soubor slicerdhub.exe bude v podadresáři dist/

Jak funguje

Pokud aplikace spustíte ručně, otevře se GUI s možností přidat slicery nebo možnost uložit soubor.

Pokud je SlicerDHub spojen s exportem (ve Fusion 360), předá soubor jako argument a po zvolení sliceru se tento soubor předá sliceru.

Nastavení

V aplikaci můžete zapnout/vypnout automatické zavření po spuštění sliceru

Možnost změnit motiv (světlý, tmavý, systémový)

Data se ukládají do ~/.slicerdhub/config.json

Autor

David H (HDaveSoft)

Ikonka a grafické zpracování: Vygenerováno s pomocí AI, upraveno pro potřeby projektu.

Licence

Tento projekt je licencován pod licencí Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0).

To znamená:

Můžete aplikaci volně používat a upravovat pro nekomerční účely

Musíte zachovat odkaz na původního autora (HDaveSoft) a tuto licenci

Nesmíte software prodávat ani vybírat dary bez uvedení původního autora a odkazu: https://coff.ee/hdavesoft

Změny musí být šířeny pod stejnou licencí

Podrobnosti: https://creativecommons.org/licenses/by-nc-sa/4.0/

TODO

Podpora drag & drop

Možnost přetáhnout STL přímo na dlaždici sliceru

Verze pro MacOS

