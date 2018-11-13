# WEE - Web Evolutionary Exploiting

## Approccio

1. Contratti
    1. Generazione dei contratti per le vulnerabilità
    1. Inferenza contratti
1. CFG sito
    1. Generazione grafo con le pagine del sito
    1. Calcolo delle distanze dai bersagli
1. Generazione sequenze di attacco
    1. Generazione popolazione iniziale (lista di liste di azioni)
        + Tracce composte da azioni random
        + Tracce utente (Selenium IDE)
    1. Algoritmo evolutivo per avvicinarsi alla vulnerabilità
        + Calcolo fitness
            + (-$\infty$, 1] -- Distanza dalla chiamata
            + (1, 0] -- Distanza su parametri

## Contesto

+ **Obiettivo**: generazione tracce di esecuzione invece esplorazione di pagine (è importante anche come si arriva alla pagina, vedi stato interno del server)
    + Generiamo tracce perchè spesso è importante anche lo stato interno del sistema (vedi pattern di pagamento)
    + Problema: generare tracce minime (da affrontare in un secondo momento)

### Possibili obiezioni

+ Tanto vale usare un crawler tradizionale!
    + No, il suo obiettivo è esplorare le pagine e farne una lista, senza fare tracce di esecuzione
+ Usiamo *mutational fuzzing* invece di GA
    + Mutational fuzzing ha senso quando sai come va fatta una cosa, GA serve quando sai cosa devi fare, ma non sai come.
+ Ha senso fare cross-over della sequenza? Cosa mi porta?
    + Worst-case scenario, mantengo le vecchie sequenze (ma rischio minimi locali)
    + Best-case scenario, riesco a comporre le sequenze relative a due pagine diverse

## TODO

+ [x] **Generazione tracce di test**
    + [x] Selenium
    + [ ] ~~Puppeteer~~
+ [ ] **Target**
    + [ ] custom Reflected XSS([target-site](target-site))
        + [x] plain html
            + [x] Pagine HTML sparse collegate da link
            + [ ] Libreria di Template non sicura in PHP
        + [x] jQuery
            + [x] Pagine che si includono usando $.get
        + [ ] AngularJS
    + [ ] custom Stored XSS ([case-study](case-study))
        + [ ] plain html
            + [x] [Pagina](case-study/form.php) con form che salva in $_SESSION
            + [x] [Pagina](case-study/target.php) che recupera il valore in $_SESSION
+ [ ] **Algoritmo genetico**
    + [x] Scelta libreria
        + [ ] ~~Implementazione custom in Python~~
        + [x] [DEAP](https://github.com/DEAP/deap)
    + [ ] Calibrazione algoritmo
        + [x] Scegliere alfabeto azioni
            + Una tra:
                + [x] {click, type, scroll, wait}: alfabeto semplice, non richiede conoscenza della pagina, ma lo spazio di possibilità potrebbe essere troppo ampio
                + [ ] ~~{interazione contestuale con elementi della pagina}: alfabeto complesso e context-sensitive, richiede conoscenza della pagina~~
            + [x] Definire encoding delle azioni
            + [ ] Definire lunghezza tracce
        + [ ] Scegliere possibili mutazioni
            + [x] Generazione traccia "sana" ([sane.py](sane.py))
            + [x] Generazione traccia di attacco ([exploit.py](exploit.py))
            + [x] Guardare quali mutazioni servono per passare da una all'altra
                + Normalmente la traccia di movimento è la stessa, mentre cambia il payload (quindi cambiano i blocchi TYPE)
            + [ ] Scegliere il numero minimo di mutazioni
        + [ ] Calcolo fitness
            + [ ] Privilegiare sequenze più corte
                * Con Stored, non sempre la sequenza più corta è la migliore
                * Spareggio fra sequenze di azioni che generano lo stesso percorso
        + [ ] Scelta popolazione iniziale
            + [x] Random
            + [x] Tracce "sane" per il sito
            + [ ] Tracce di attacco per un altro sito
        + [ ] Dimensionare valori
            + [ ] dimensione popolazione iniziale
            + [ ] cross-over
            + [ ] mutation rate
+ [ ] **Dati sperimentali**

## Link utili

+ Genetic Algorithms
    + https://github.com/MorvanZhou/Evolutionary-Algorithm
