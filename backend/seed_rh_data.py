import sqlite3
import uuid

def seed():
    conn = sqlite3.connect('data/ia_finder.db')
    cursor = conn.cursor()

    rh_data = [
        {
            "name": "FAQ - Contrat de Travail",
            "content": """
Q: Où puis-je télécharger mon contrat de travail ?
R: Vous pouvez accéder à votre contrat de travail via votre Espace salarié, dans le coffre-fort numérique. Suivez la procédure d'accès classique avec vos identifiants.

Q: Quelle est la durée de mon période d'essai ?
R: La durée de votre période d'essai dépend de votre date d'embauche, de votre type de contrat (CDI, CDD) et de la convention collective applicable. Veuillez consulter l'article 3 de votre contrat.

Q: Comment modifier mon adresse postale ?
R: Pour modifier vos données personnelles, veuillez remplir le Formulaire RH disponible sur l'intranet. Une validation sera effectuée et l'impact sera visible sur vos prochains bulletins de paie.

Q: Qui est mon responsable hiérarchique N+1 ?
R: Vous pouvez trouver cette information organisationnelle sur l'Organigramme de l'entreprise, votre fiche de poste, ou l'annuaire interne.

Q: Puis-je obtenir une attestation employeur ?
R: La demande de document se fait via le portail RH. La procédure prend généralement un délai de traitement de 48h, et le format est envoyé par PDF/email.

Q: Je souhaite passer à temps partiel, quelle est la procédure ?
R: La modification contractuelle requiert plusieurs étapes : une demande écrite de votre part, un entretien RH, puis la signature d'un avenant au contrat en respectant le délai de prévenance.

Q: Mon contrat arrive à échéance, que se passe-t-il ?
R: Pour la gestion de fin de contrat, nous devons vérifier votre type de contrat (CDD/CDI/intérim). Nous vous expliquerons le renouvellement possible ou la procédure de rupture.

Q: Je change de poste en interne, mon ancienneté est-elle conservée ?
R: Dans le cadre d'une mobilité interne, nous confirmons la continuité d'ancienneté. Cela n'a aucun impact sur vos droits acquis (congés, prévoyance, etc.).
            """,
            "roles": "user,manager,rh_admin"
        },
        {
            "name": "FAQ - Paie & Rémunération",
            "content": """
Q: Quand suis-je payé ?
R: La date de versement de la rémunération (mensuelle/bi-mensuelle) se fait généralement le 28 du mois, variable selon les délais bancaires.

Q: Où trouver mon bulletin de paie ?
R: Votre accès documentaire se fait par le Portail salarié ou l'application mobile. Il s'agit de notre système d'archivage légal.

Q: Pourquoi mon salaire net est-il différent ce mois-ci ?
R: La compréhension de variation de votre salaire net peut s'expliquer par les heures supplémentaires, les absences, les primes, ou les cotisations variables.

Q: Comment sont calculées mes heures supplémentaires ?
R: Vos heures supplémentaires sont calculées sur la base de notre taux de majoration, des seuils légaux, de la convention collective, et suite à la validation de votre manager.

Q: Puis-je recevoir ma paie sur un autre compte bancaire ?
R: Pour toute modification de coordonnées bancaires, veuillez suivre la procédure de changement avec validation RH. Il y a un délai de prise en compte pour la prochaine paie.

Q: Je n'ai pas reçu ma paie à la date prévue, que faire ?
R: Il s'agit d'un incident critique. Nous allons vérifier le statut du virement, identifier la cause (banque, erreur interne) et vous proposer une solution immédiate.

Q: Mon bulletin de paie comporte une erreur, comment le faire corriger ?
R: Veuillez ouvrir un ticket paie pour demander une rectification administrative. Des justificatifs pourront vous être demandés avec un délai de régularisation pour l'émission d'un nouveau bulletin.

Q: Comment sont calculées mes primes variables ?
R: Dans un souci de transparence, vos primes s'expliquent par divers critères (objectifs, performance, ancienneté). Nous vous fournirons le détail du calcul ou vous orienterons vers le manager.
            """,
            "roles": "user,manager,rh_admin"
        },
        {
            "name": "FAQ - Congés & Absences",
            "content": """
Q: Combien de jours de congés me reste-t-il ?
R: Vous pouvez consulter votre solde de congés (droits acquis, consommés, reportés) directement via l'interface SIRH.

Q: Comment poser un jour de congé ?
R: La procédure de demande utilise notre outil de demande (portail/app) et requiert la validation de votre manager selon le délai de prévenance en vigueur.

Q: Quels sont les jours fériés chômés dans l'entreprise ?
R: L'information de notre calendrier se base sur la liste officielle et les spécificités locales/conventionnelles appliables.

Q: Puis-je poser mes congés en une seule fois ?
R: Les règles de prise de congés sont définies par la politique interne et les contraintes opérationnelles. Un accord hiérarchique est indispensable.

Q: Comment déclarer un arrêt maladie ?
R: La procédure d'absence impose un délai de déclaration strict. Vous devez fournir votre avis d'arrêt à vos interlocuteurs (RH, sécu).

Q: Je souhaite poser des congés sans solde, est-ce possible ?
R: Pour les congés exceptionnels non-payés, nous devons vérifier votre éligibilité (ancienneté, motif). La procédure impactera vos droits et votre rémunération.

Q: Mon arrêt maladie est prolongé, que dois-je faire ?
R: En cas d'absence longue durée, vous devez nous transmettre le nouvel arrêt. Cela aura un impact sur la paie, le maintien de salaire, et le retour progressif si applicable.

Q: Puis-je récupérer des jours de RTT non pris ?
R: Pour la gestion des compteurs temps, nous devons vérifier la politique de report ou de monétisation. Nous vous expliquerons les délais et la procédure de demande.
            """,
            "roles": "user,manager,rh_admin"
        }
    ]

    print("Insertion des documents RH...")
    
    cursor.execute("SELECT id FROM users LIMIT 1")
    user_row = cursor.fetchone()
    if not user_row:
        print("Aucun utilisateur trouvé.")
        return
    user_id = user_row[0]

    for doc in rh_data:
        source_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO sources (id, user_id, name, type, content, is_active, is_archived, allowed_roles)
            VALUES (?, ?, ?, ?, ?, 1, 0, ?)
        ''', (source_id, user_id, doc["name"], 'document', doc["content"], doc["roles"]))
    
    conn.commit()
    conn.close()
    print("Documents insérés avec succès.")

if __name__ == '__main__':
    seed()
