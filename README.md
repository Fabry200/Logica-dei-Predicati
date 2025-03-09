# Analisi Ricorsiva di Espressioni Logiche

Questo file contiene l'implementazione di un sistema basato su un albero binario ricorsivo per l'analisi e la valutazione di espressioni logiche. È stato sviluppato per interpretare, costruire e valutare in maniera ricorsiva formule espresse in una notazione compatta, traducendo operatori e predicati in una struttura ad albero.

## Struttura del Codice

- **Classe `Nodo`**  
  Rappresenta un nodo dell'albero e contiene:
  - **Attributi**:  
    - `name`: il simbolo o l'espressione associata al nodo (può essere un operatore logico, un predicato o un quantificatore).
    - `left` e `right`: i figli sinistro e destro, utili per rappresentare espressioni binarie.
    - `parent`: riferimento al nodo padre, per permettere il passaggio dei dati in maniera ricorsiva verso l’alto.
    - `vector`: una lista che memorizza i risultati parziali o booleani, utilizzata durante la valutazione dell'espressione.
    
  - **Metodi principali**:
    - `stampa`: restituisce una rappresentazione in formato stringa dell'albero, con indentazione che evidenzia la struttura gerarchica.
    - `values`: valuta il nodo sostituendo le variabili presenti nel nome in base a un dizionario fornito e calcola il risultato usando `eval()`.
    - `ld_values`: genera un insieme di assegnazioni (sottoinsiemi dell'universo ristretto) per i predicati atomici, utilizzando il prodotto cartesiano e verificando una relazione.
    - `Truthcheck`: controlla la veridicità di un predicato, confrontando i valori ottenuti con quelli attesi, e aggiorna il vettore booleano.
    - `update_vector` e `myfunc`: metodi che propagano e aggregano i risultati (i vettori) dai nodi foglia fino alle radici, gestendo in modo ricorsivo il passaggio dei valori.
    - `opera`: applica gli operatori logici (AND, OR, NOT) combinando i vettori dei figli attraverso le funzioni `min`/`max` (o direttamente con `and`, `or`, `not`), eseguendo una valutazione logica.
    - `finalmente`: valuta il risultato finale dell’espressione logica; se il nodo rappresenta un quantificatore (identificato da 'V' o 'E'), usa rispettivamente `all()` o `any()` sui valori aggregati e stampa il risultato.

- **Funzione `costruisci`**  
  Questa funzione analizza una stringa che rappresenta l’espressione logica e costruisce ricorsivamente l’albero:
  - Utilizza un ciclo e l’istruzione `match` per interpretare caratteri e simboli (ad esempio, parentesi, operatori logici come `A` per AND, `O` per OR, `N` per NOT, e predicati come `P[...]`).
  - Imposta i collegamenti tra nodi (figlio sinistro, destro e riferimento al padre) per riflettere la struttura logica dell’espressione.

- **Funzione `main` e `build`**  
  - **Definizione delle Espressioni**:  
    Vengono definite diverse stringhe (A, B, C, D) che rappresentano differenti espressioni logiche. Queste stringhe vengono opportunamente manipolate (sostituendo "and", "or", "not") per uniformare la notazione.
  - **Costruzione e Valutazione**:  
    Per ogni espressione, viene creato un oggetto `Nodo` e costruito l’albero con `costruisci`. Successivamente, si esegue:
    - La generazione dell'insieme di valori (con `ld_values`),
    - La verifica dei predicati tramite `Truthcheck`,
    - L'aggiornamento e propagazione dei vettori di verità con `update_vector` e `myfunc`,
    - L'applicazione degli operatori logici con `opera` e infine la valutazione finale con `finalmente`.

## Esempio d'Uso

Per valutare un’espressione logica:
1. **Definisci l'espressione**:  
   Ad esempio, l'espressione `'(EyP[xy])'` rappresenta un predicato con quantificatore.  
2. **Costruisci l'albero**:  
   Usa la funzione `costruisci` per convertire la stringa in una struttura ad albero.
3. **Valuta l'espressione**:  
   - Genera l'insieme di assegnazioni per il predicato con `ld_values`.
   - Verifica le condizioni logiche con `Truthcheck`.
   - Propaga i risultati tramite `update_vector` e `myfunc`.
   - Applica gli operatori logici con `opera`.
   - Determina il risultato finale (vero o falso) con `finalmente`.

Questo approccio ricorsivo permette di analizzare ed eseguire il calcolo di espressioni logiche complesse, supportando l'integrazione di quantificatori e operatori logici in maniera modulare e flessibile.

---

Questo file è un esempio pratico di come strutturare e valutare espressioni logiche in maniera ricorsiva, utile per applicazioni in cui si desidera modellare sistemi di inferenza o interpretazione di formule logiche.
