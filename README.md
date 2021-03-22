# Control_Room_Simulator

## Cel Projektu

Tematem zadania szóstego jest napisanie aplikacji, będącej symulatorem stanowiska dyspozytorskiego „linii produkcyjnej”. Program ten ma zawierać elementy diagnostyki nadzorowanego „procesu produkcji” jak i autodiagnostyki operatora czuwającego nad prawidłowym przebiegiem „produkcji”. Wykorzystując dostępne informacje na temat parametrów pracy komputera PC (np. temperatury rdzenia procesora, stopnia wykorzystania procesora, prędkości obrotowych wentylatorów itp.) oraz generatory liczb losowych i timery, zasymulować parametry kontrolowanego „procesu produkcyjnego”. Należy przewidzieć obsługę pojawiających się losowo awarii oraz przekroczeń granicznych wartości wybranych parametrów procesu - np. po przekroczeniu granicznej temperatury obudowy silnika należy włączyć dodatkowy wentylator lub zwolnić tempo pracy linii produkcyjnej itp. O wszystkich wyjątkowych zdarzeniach i wymaganych działaniach, operator musi być informowany za pośrednictwem odpowiedniego zestawu komunikatów. Program powinien zawierać okno logowania do aplikacji i na bieżąco badać obecność oraz „przytomność” operatora. Element autodiagnostyczny powinien polegać na okresowym pojawieniu się komunikatu informującego o konieczności potwierdzenia obecności przez wciśnięcie wybranego klawisza. W przypadku braku potwierdzenia, np. przez co najmniej 30 sekund, powinno następować uruchomienie alarmu i wylogowanie operatora z systemu. 

## Realizacja

Program został zrealizowany z wykorzystaniem języka Python 3.7 w środowisku PyCharm Community Edition 2019.3.4 x64.

Stworzono aplikację umożliwiającą symulację pracy przy stanowisku dyspozytorskim “linii produkcyjnej” przy połączeniu diagnostyki nadzorowanego procesu produkcji z autodiagnostyką operatora pełniącego pieczę nad poprawnością przebiegu “produkcji”.

W programie wykorzystano moduł PyQt5 5.14.2 w celu stworzenia gui aplikacji.

Zgodnie z założeniami zadania, symulator wykorzystując dostępne informacje na temat parametrów pracy układu (wykorzystanie procesora, temperatura procesora oraz prędkość obrotowa wentylatorów) przy jednoczesnym wykorzystaniu generatorów liczb losowych oraz timerów umożliwia symulację parametrów kontrolowanego procesu produkcyjnego. 

Cała symulacja jest zautomatyzowana, program sam jest w stanie samodzielnie balansować we właściwych “widełkach” wartości parametrów na podstawie ich analizy, poprzez włączanie dodatkowych wentylatorów. Zgodnie z polecenie, o wszelkich zdarzeniach użytkownik informowany jest w postaci komunikatu wyświetlającego się w okienku QTextEdit. 

<img src="https://raw.githubusercontent.com/MacKur/Control_Room_Simulator/main/Symulator.png">


Program wymaga zalogowania się przez użytkownika przyciskiem ON, a następnie na bieżąco bada obecność operatora poprzez wyświetlenie komunikatu o konieczności zaznaczenia swojej obecności czerwonym przyciskiem widocznym na powyższych zrzucie ekranu. W przypadku braku potwierdzenia obecności, program wylogowuje użytkownika i wyłącza proces produkcyjny.
