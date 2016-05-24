# latin-authorship
Authorship attribution in Latin using LIBSVM and CLTK

Feature extraction in Python using CLTK and machine learning using Octave/LIBSVM in order to find authorship of dubiously-sourced Classical Latin texts (_De Bello Africo_, etc)

The `.lat` files are intermediary feature files for each text.

Data used uses eight different classical prosaic authors: Caesar, Aulus Hirtius (who often wrote for Caesar), Cicero, Suetonius, Sallust, Livy, Seneca the Younger, and Tacitus.

The training set uses the following works:
* Caesar - _De Bello Gallico_ books 1-7, _De Bello Civili_ books 1-2
* Hirtius - _De Bello Gallico_ book 8, _De Bello Alexandrino_
* Cicero - _In Verrem_, _In Catilinam_, _Pro Archia Poeta_, _De Oratore_, _Epistulae ad Atticum_
* Suetonius - _De Vitis Caesarum_ Iulus-Titus, _De Grammaticis_, _De Rhetoribus_
* Sallust - _Bellum Catilinae_, _Bellum Iugurthinum_
* Livy - _Ad Urbe Condita Libre_ books 1-9, 21-45
* Seneca Minor - _Quaestiones Naturales_, _De Beneficiis_, _De Ira_ books 1-2
* Tacitus - _Annales_, _Historiae_, _Germania_

The cross-validation set uses the following works:
* Caesar - _De Bello Civili_ book 3
* Cicero - _Pro Quinctio_, _Pro Caecina_, _De Re Publica_ book 1
* Suetonius - _De Vitis Caesarum_ Domitian
* Sallust - _Historiae_
* Livy - _Ad Urbe Condita Libre_ book 10
* Seneca Minor - _De Ira_ book 3
* Tacitus - _De Vita et Moribus Iulii Agricolae_

The testing (unknown set) uses the following works:
* _De Bello Africo_ - either Caesar, Hirtius, or someone else entirely
* _De Bello Hispaniensi_ - either Caesar, Hirtius, or someone else entirely
* _Invectiva in Ciceronem_ - attributed to Sallust but questioned
* _Dialogus de Oratoribus_ - attributed to Tacitus but questioned, also meant to imitate Cicero
* _Metamorphoses_, book 1 by Apuleius - to test what happens when the author is not in the trained author list
* _Naturalis Historiae_, book 5 by Pliny the Elder - to test what happens when the author is not in the trained author list
* _Res Gestae_, book 1 by Augustus - to test what happens when the author is not in the trained author list

Citations:

> Kyle P. Johnson et. al.. (2014-2016). CLTK: The Classical Language Toolkit. DOI http://dx.doi.org/10.5281/zenodo.51144

> Chih-Chung Chang and Chih-Jen Lin, LIBSVM : a library for support vector machines. ACM Transactions on Intelligent Systems > and Technology, 2:27:1--27:27, 2011. Software available at http://www.csie.ntu.edu.tw/~cjlin/libsvm
