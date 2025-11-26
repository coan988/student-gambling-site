//Dokument
#set text(lang: "de", size: 12pt, font: "Arial")
#set document(
  title: "Internetauftritt Studentenkasino",
  author: "Elijah Mossmann, Timo Manz, Michael Zerner, Corvin Annen",
)

#set page(
  paper: "a4",
  margin: (top: 4cm, bottom: 2cm, left: 1.5cm, right: 1.5cm),
  numbering: "I",
  footer: none,
)
#set heading(outlined: true)

#set cite(style: "styles/chicago-s-notes-bibliography.csl")

//Deckblatt
#page[
  #align(center)[
    #text(2.4em, weight: "bold")[
      Internetauftritt Studentenkasino
    ]
    #v(1em)

    #text(1.4em)[
      Projektdokumentation
    ]
  ]

  #v(8em)

  #align(center)[
    #text(1em)[
      Studienjahrgang: 2024\
      Kurs: A\

      #v(1em)

      Fakultät: Wirtschaft\
      Studiengang: Wirtschaftinformatik\
      Modul: Fallstudien / Herr Schulik\
      Semester: Sommersemester 2025
    ]
  ]

  #v(6em)

  #align(left)[
    #text(1em, weight: "bold")[Projektteam:]

    #text(1em)[
      Corvin Annen – Projektleitung\
      Elijah Mossmann – Backend\
      Timo Manz – Frontend\
      Michael Zerner – Hosting & Deployment
    ]
  ]

  #v(6em)

  #align(right)[
    #text(1em)[
      DHBW Villingen-Schwenningen\
      Abgabedatum: 27.11.2025
    ]
  ]
  #image("DHBW Logo.png")
]

#pagebreak()

#set page(margin: (top: 4cm, bottom: 2cm, left: 4cm, right: 2cm))

//Inhaltsverzeichniss
#outline(
  title: "Inhaltsverzeichnis",
  depth: 3,
)
#pagebreak()

//Kopfzeile - Verzeichnisse
#counter(page).update(3)
#set page(
  header: context {
    [
      #h(1fr)
      #counter(page).display()
    ]
  },
)
//Abkürzungsverzeichnis
= Abkürzungsverzeichnis
#pagebreak()

//Abbildungsverzeichnis
= Abbildungsverzeichnis
#pagebreak()

//Kopfzeile - Text
#counter(page).update(1)

#let currentH(level: 1) = {
  let elems = query(selector(heading.where(level: level)).after(here()))

  if elems.len() != 0 and elems.first().location().page() == here().page() {
    return elems.first().body
  } else {
    elems = query(selector(heading.where(level: level)).before(here()))
    if elems.len() != 0 {
      return elems.last().body
    }
  }
}

#set page(numbering: "1", header: context {
  [
    #currentH(level: 1)
    #h(1fr)
    #counter(page).display()
  ]
})

//Überschriften
#set heading(numbering: "1.1")
#show heading.where(level: 1): it => {
  set block(below: 1.5em, above: 2em)
  it
}
#show heading.where(level: 2): it => {
  set block(below: 1em, above: 1.5em)
  it
}
#show heading.where(level: 3): it => {
  set block(below: 0.8em, above: 1.2em)
  it
}

//Text
#set text(12pt, font: "Arial")

#set par(
  justify: true,
  leading: 1em,
)

= Einleitung
== Problemstellung
#par[Die vorliegende Arbeit behandelt die Konzeption und Umsetzung einer Webanwendung, die sowohl eine gute Performence wie auch eine komfortable skalierbarkeit enthalten soll. Moderne Webprojekte stehen vor der Herausforderung, gleichzeitig nutzerfreundlich, zuverlässig und bei wachsender Nutzung skalierbar zu bleiben. Besonders bei Anwendungen, die spielerische Elemente oder Wettbewerbsmechanismen enthalten, steigt die technische Komplexität deutlich, da Echtzeitinteraktionen und schnelle Datenverarbeitung erforderlich sind. Ein weiteres Problem ist die sichere Verwaltung von Benutzerdaten und Spielwährungen, da diese Systeme potenzielle Angriffsziele darstellen. Gleichzeitig muss die Oberfläche intuitiv gestaltet werden, um auch Studierende ohne technische Vorkenntnisse eine Speilerfahrung zu bieten. Die Plattform soll darüber hinaus flexibel erweiterbar sein, sodass neue Spiele, Module oder Funktionen ohne große strukturelle Umbauten integriert werden können. Zusätzlich wird im Rahmen der Arbeit untersucht, welche Marketingmethoden angewannt werden müssen um die gewünschte Zielgruppe zu erreichen. Insgesamt besteht die zentrale Herausforderung darin, eine robuste, skalierbare und benutzerorientierte Webanwendung zu entwickeln, die sowohl technisch als auch organisatorisch langfristig betreibbar ist.]
== Zielsetzung
#par[Ziel der Arbeit ist die Entwicklung eines sicheren, skalierbaren und modular aufgebauten Studentencasinos, das durch spielerische Elemente den Wettbewerb zwischen den Nutzern fördert. Dazu wird eine fiktive Spielwährung eingeführt, der „Coin“, der als zentrale Ressource für alle Spiele und Mechaniken dient. Ein übergreifendes Punktesystem soll alle Spieler anhand ihrer Coin-Anzahl in einer Rangliste absteigend sortieren und so einen dauerhaften Anreiz zur Teilnahme schaffen. Durch verschiedene Minigames erhalten die Nutzer die Möglichkeit, ihre Coins zu vermehren, wodurch Dynamik und Variation entstehen. Die Plattform wird so entworfen, dass neue Spiele ohne größere strukturelle Anpassungen integriert werden können, was langfristige Erweiterbarkeit sicherstellt. Ein weiterer Schwerpunkt liegt auf der Sicherheit des Systems, insbesondere der korrekten und manipulationssicheren Verwaltung der Spielwährung. Zusätzlich berücksichtigt die Zielsetzung Aspekte wie Nutzerfreundlichkeit, klare Interface-Gestaltung und die Schaffung eines motivierenden Spielerlebnisses. Insgesamt soll eine Plattform entstehen, die stabil, attraktiv und technisch sauber umgesetzt ist.]
== Aufbau
#par[Die Arbeit gliedert sich in mehrere Hauptkapitel, die den gesamten Projektverlauf von der Planung bis zur Reflexion strukturiert darstellen. Nach der Einleitung folgt das Kapitel Projektmanagement, in dem die gewählte Methodik, die Organisation des Teams sowie Kommunikations- und Planungsprozesse beschrieben werden. Anschließend widmet sich das Kapitel Konzeption den ermittelten Anforderungen, der technologischen Auswahl und der Ausarbeitung der Gesamtarchitektur des Systems. Die darauf folgenden Kapitel Backend und Frontend beschreiben im Detail die technische Umsetzung, die verwendeten Frameworks und die Art, wie Logik, Datenhaltung und Benutzeroberfläche miteinander interagieren. Im Kapitel Hosting wird erläutert, wie die Anwendung bereitgestellt, versioniert und deployt wird, um eine stabile und skalierbare Umgebung sicherzustellen. Danach folgt das Kapitel Projektergebnis/Reflexion, das die wesentlichen Resultate zusammenfasst und den Entwicklungsprozess hinsichtlich Effizienz, Herausforderungen und gewonnener Erfahrungen bewertet. Die Struktur der Arbeit ermöglicht eine klare Nachvollziehbarkeit der Entscheidungen sowie der technischen und organisatorischen Umsetzung des Projekts. Dadurch wird sowohl die fachliche Tiefe als auch die praktische Relevanz der Arbeit sichtbar gemacht.]
#pagebreak()
= Projektmanagement
#par[In dem Kapitel Projektmanagement werden die organisatorischen und methodischen Grundlagen des Projekts beschrieben. Es umfasst die gewählte Projektmethodik, die Kommunikations- und Austauschprozesse innerhalb des Teams sowie die Planung des Projekts. Ziel dieses Kapitels ist es, einen klaren Überblick über die Strukturierung und Steuerung des Projekts zu geben, um die Effizienz und den Erfolg der Umsetzung sicherzustellen.]
== Projektmethodik
#par[Für die Umsetzung des Projekts wurde eine Iterative, agile Projektmethode mit regelmäßigen Meetings gewählt. Diese Methode ermöglicht es, flexibel auf Änderungen zu reagieren und kontinuierlich Verbesserungen vorzunehmen. Durch kurze Entwicklungszyklen konnten Anforderungen schnell umgesetzt und getestet werden, was die Qualität des Endprodukts erhöhte. Die agile Methodik förderte zudem die Zusammenarbeit im Team, da regelmäßige Abstimmungen und Feedbackrunden eingeplant wurden. Insgesamt trug diese Vorgehensweise dazu bei, das Projekt effizient zu steuern und den Fokus auf die wichtigsten Ziele zu legen.]
== Austausch
#par[Die Kommunikation und der Austausch im Projektteam erfolgten überwiegend über eine gemeinsame WhatsApp-Gruppe sowie durch persönliche Gespräche im Anschluss an Vorlesungen. Für die kontinuierliche Abstimmung kamen OneNote und verschiedene Funktionen von GitHub zum Einsatz. GitHub ermöglichte es, Kommentare direkt im Code zu hinterlassen und Aufgaben eindeutig zuzuweisen. Zur Planung und Nachverfolgung einzelner Arbeitspakete wurde der „Issues“-Bereich von GitHub genutzt, der eine strukturierte Verwaltung von Milestones, Tasks und Fehlerberichten erlaubte. Auf dieser Grundlage konnten Fortschritte transparent dokumentiert und Prioritäten festgelegt werden. Ergänzend fanden wöchentliche Meetings über Discord statt, um komplexere Fragestellungen zu besprechen, Entscheidungen zu treffen und den direkten Austausch zu stärken. Zentrale Projektdokumente und relevante Informationen wurden in OneNote abgelegt, sodass alle Teammitglieder jederzeit Zugriff auf den aktuellen Wissensstand hatten. Durch die kombinierte Nutzung dieser Werkzeuge wurde eine transparente und effiziente Kommunikation ermöglicht, was wesentlich zur erfolgreichen Zusammenarbeit im Projekt beitrug.]
== Planung
#par[Die Planung bildete den organisatorischen Rahmen des Projekts und strukturierte die Zusammenarbeit über den gesamten vierwöchigen Bearbeitungszeitraum. Zu Beginn wurden Zuständigkeiten definiert sowie Anforderungen und Ziele des geplanten Internetauftritts festgelegt. Darauf aufbauend entstand eine Projektstruktur, aus der sich Aufgaben, Meilensteine und zeitliche Prioritäten ableiten ließen. Die anschließende Feinplanung diente als Grundlage für die Ausarbeitung der Rollen, die Erstellung eines realistischen Zeitplans sowie die Festlegung zentraler Meilensteine. Während der Umsetzung wurde diese Planung kontinuierlich überprüft und bei Bedarf angepasst, um den engen Zeitrahmen effizient zu nutzen.]
=== Rollenverteilung
#par[Die Rollenverteilung im Projektteam wurde klar definiert, um eine effiziente Zusammenarbeit und Verantwortungsübernahme zu gewährleisten. Corvin Annen übernahm die Projektleitung und koordinierte sämtliche organisatorischen Abläufe. Dazu gehörten Terminabsprachen, die Abstimmung zwischen den Entwicklungsbereichen sowie die Überwachung des Projektfortschritts.
  Elijah Mossmann war für die Backend-Entwicklung verantwortlich. Sein Aufgabenbereich umfasste die Implementierung der API-Strukturen, die Anbindung der Datenbank sowie die Sicherstellung der funktionalen Logik. Timo Manz leitete die Frontend-Entwicklung. Er konzipierte die Benutzeroberfläche, setzte UI-Komponenten um und sorgte dafür, dass Funktionalität und Gestaltung konsistent ineinandergreifen. Michael Zerner betreute Hosting und Deployment. Er kümmerte sich um die Serverumgebung, richtete das Hosting ein und verantwortete die Bereitstellung der Anwendung einschließlich Tests der Live-Version. Diese Rollenverteilung gewährleistete, dass Arbeitsbereiche klar abgegrenzt waren und jedes Mitglied zielgerichtet beitragen konnte.]
=== Zeitplan
#par[Für das vierwöchige Projekt wurde ein komprimierter, aber realistischer Zeitplan ausgearbeitet. Die erste Woche war der Konzeption gewidmet: Klärung der Anforderungen, Auswahl geeigneter Technologien und Festlegung der Systemarchitektur. In den beiden folgenden Wochen erfolgte die parallele Entwicklung von Backend und Frontend, begleitet vom Aufbau der Datenbank und der Implementierung grundlegender UI-Elemente. In der letzten Woche standen Hosting, Integrationstests und Optimierungen im Vordergrund. Regelmäßige Abstimmungen erlaubten es, Fortschritte zu kontrollieren und den Zeitplan situativ anzupassen, ohne die Zieltermine zu gefährden.]
=== Meilensteine
#par[Die Meilensteine des Projekts wurden strategisch festgelegt, um den Fortschritt zu überwachen und sicherzustellen, dass die wichtigsten Ziele erreicht werden. Zu den zentralen Meilensteinen gehörten die Fertigstellung der Konzeptionsphase, die Implementierung des Backends und Frontends, die Entwicklung der Datenbankstruktur sowie die Bereitstellung der Anwendung im Hosting-Umfeld. Jeder Meilenstein markierte einen bedeutenden Fortschritt im Projektverlauf und diente als Grundlage für die nächsten Schritte. Durch die klare Definition dieser Meilensteine konnte das Team den Überblick behalten und sicherstellen, dass alle Aufgaben termingerecht abgeschlossen wurden.]
#pagebreak()
= Konzeption
#par[Das Kapitel Konzeption beschreibt die grundlegenden Überlegungen und Entscheidungen, die der technischen Umsetzung des Projekts zugrunde liegen. Es umfasst die Analyse der Anforderungen, die Auswahl der technologischen Komponenten sowie die Ausarbeitung der Gesamtarchitektur des Systems. Ziel dieses Kapitels ist es, eine klare und nachvollziehbare Grundlage für die anschließende Entwicklung zu schaffen.]
== Anforderungen
#par[Die Anforderungen an den Internetauftritt des Studentencasinos wurden sorgfältig analysiert, um eine benutzerfreundliche, sichere und skalierbare Plattform zu schaffen. Funktionale Anforderungen umfassen die Implementierung eines Punktesystems mit einer fiktiven Spielwährung („Coins“), die Integration verschiedener Minigames zur Coin-Generierung sowie die Anzeige einer Rangliste basierend auf der Coin-Anzahl der Nutzer. Darüber hinaus soll die Plattform modular aufgebaut sein, um zukünftige Erweiterungen und neue Spiele problemlos integrieren zu können. Nicht-funktionale Anforderungen beinhalten Aspekte wie Sicherheit bei der Verwaltung der Spielwährung, Performance-Optimierung für eine reibungslose Nutzererfahrung sowie eine intuitive Benutzeroberfläche. Zusätzlich wurde Wert auf eine klare und ansprechende Gestaltung gelegt, um die Zielgruppe der Studierenden effektiv anzusprechen. Insgesamt sollen diese Anforderungen sicherstellen, dass die Plattform sowohl technisch robust als auch attraktiv für die Nutzer ist.]
== Technologische Entscheidungen
#par[Die technologischen Entscheidungen für die Umsetzung des Studentencasinos wurden auf Basis der Anforderungen und Zielsetzungen des Projekts getroffen. Für das Backend wurde das Django-Framework in Python gewählt, da es eine robuste Struktur für die Entwicklung von Webanwendungen bietet und eine einfache Integration mit Datenbanken ermöglicht. Django's integriertes Authentifizierungssystem erleichtert zudem die sichere Verwaltung von Benutzerdaten.@Django Für das Frontend fiel die Wahl auf React, da es eine komponentenbasierte Architektur bietet, die eine flexible und wiederverwendbare Gestaltung der Benutzeroberfläche ermöglicht. Vite wurde als Bundler eingesetzt, um schnelle Entwicklungszyklen und effizientes Build-Management zu gewährleisten. Als Datenbank wurde SQLite verwendet, da es leichtgewichtig ist und sich gut für die Anforderungen des Projekts eignet, mit der Möglichkeit, bei Bedarf auf leistungsfähigere Systeme wie MySQL oder PostgreSQL zu skalieren. Diese technologischen Entscheidungen tragen dazu bei, eine stabile, skalierbare und benutzerfreundliche Plattform zu schaffen.]
== Gesamtarchitektur
//Grafik draus bauen
Backend (API)
- Framework: Django (Python)
- Sprache: Python
- API Endpoints:
  - `GET /api/users`
  - `POST /api/users`
  - `GET /api/posts`
- Authentifizierung: Django Auth System
- Geschäftslogik: Validierung und Autorisierung durch Django-Modelle und Middleware
- Datenbank: SQLite (mit Django ORM)
Frontend (Client)
- Framework: React (mit Vite als Bundler)
- Sprache: JavaScript
- Wichtige Komponenten:
  - UI-Komponenten: React-Komponenten, Seiten
  - Datenabfrage: Client-seitiges Fetching mit AJAX
  - Navigation: React Router für client-seitige Navigation
Datenbank
- Datenbank: SQLite (kann für Produktion auf MySQL/PostgreSQL erweitert werden)
- Protokoll: SQL
- Datenbank-Komponenten: Tabellen, Indizes, Constraints, verwaltet durch Django ORM
UI-Komponenten
- Sprache: HTML, CSS, JavaScript
- Framework: React
- Server-Side Rendering: Optional, mit Next.js für SSR (nicht im Repo explizit genutzt)
//Klassendiagramm bauen
= Backend
== API-Design
== Datenbankmodell

= Frontend
== Technologie-Stack
== Komponentenstruktur

= Hosting
== Server-/Hosting-Modell
== Deployment-Prozess
= Projektergebnis/Reflexion

= Anhang
= Literaturverzeichnis
#bibliography(
  (
    "bib/konzept.bib",
    "bib/backend.bib",
    "bib/frontend.bib",
    "bib/hosting.bib",
  ),
  title: none,
)
