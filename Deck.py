# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 15:41:39 2025

@author: Toxito
"""

import random

class Deck:
    def __init__(self):
        # Initialize the cards as a list of numbers from 0 to 21 (22 Major Arcana)
        self.cards = list(range(0, 22))
        self.original_cards = self.cards.copy()  # Guardar una copia del mazo original para reiniciar
        # Dictionary to store predictions for each card (upright and reversed)
        self.predictions = {}
        # Dictionary to store image paths for each card
        self.card_images = {}

        # Assign image paths and predictions for each card
        for card in self.cards:
            match card:
                case 0:
                    self.card_images[card] = 'Cards/0. The Fool.png'
                    self.predictions[card] = {
                        "upright": "The Fool: A new beginning full of adventure, embrace the unknown.",
                        "reversed": "The Fool (Reversed): Recklessness and poor decisions may lead to trouble."
                    }
                case 1:
                    self.card_images[card] = 'Cards/1. The Magician.png'
                    self.predictions[card] = {
                        "upright": "The Magician: You have the power and tools to achieve your goals.",
                        "reversed": "The Magician (Reversed): Manipulation or lack of focus hinders your potential."
                    }
                case 2:
                    self.card_images[card] = 'Cards/2. The Priestess.png'
                    self.predictions[card] = {
                        "upright": "The Priestess: Listen to your intuition, secrets will be revealed.",
                        "reversed": "The Priestess (Reversed): Hidden truths or ignored intuition cause confusion."
                    }
                case 3:
                    self.card_images[card] = 'Cards/3. The Empress.png'
                    self.predictions[card] = {
                        "upright": "The Empress: Abundance, creativity, and maternal care are present.",
                        "reversed": "The Empress (Reversed): Neglect or stifled creativity may block growth."
                    }
                case 4:
                    self.card_images[card] = 'Cards/4. The Emperor.png'
                    self.predictions[card] = {
                        "upright": "The Emperor: Structure and authority will guide you to stability.",
                        "reversed": "The Emperor (Reversed): Rigidity or lack of control creates chaos."
                    }
                case 5:
                    self.card_images[card] = 'Cards/5. The Hierophant.png'
                    self.predictions[card] = {
                        "upright": "The Hierophant: Tradition and spiritual values are important now.",
                        "reversed": "The Hierophant (Reversed): Rebellion against norms may cause disruption."
                    }
                case 6:
                    self.card_images[card] = 'Cards/6. The Lovers.png'
                    self.predictions[card] = {
                        "upright": "The Lovers: Important decisions in love or relationships.",
                        "reversed": "The Lovers (Reversed): Disharmony or misalignment in relationships."
                    }
                case 7:
                    self.card_images[card] = 'Cards/7. The Chariot.png'
                    self.predictions[card] = {
                        "upright": "The Chariot: Move forward with determination towards your goals.",
                        "reversed": "The Chariot (Reversed): Lack of direction or control slows progress."
                    }
                case 8:
                    self.card_images[card] = 'Cards/8. Justice.png'
                    self.predictions[card] = {
                        "upright": "Justice: Balance and fair consequences for your actions.",
                        "reversed": "Justice (Reversed): Injustice or imbalance affects your situation."
                    }
                case 9:
                    self.card_images[card] = 'Cards/9. The Hermit.png'
                    self.predictions[card] = {
                        "upright": "The Hermit: Seek solitude to reflect and find wisdom.",
                        "reversed": "The Hermit (Reversed): Isolation or withdrawal becomes excessive."
                    }
                case 10:
                    self.card_images[card] = 'Cards/10. Wheel of Fortune.png'
                    self.predictions[card] = {
                        "upright": "Wheel of Fortune: Unexpected changes, destiny is in motion.",
                        "reversed": "Wheel of Fortune (Reversed): Setbacks or resistance to change."
                    }
                case 11:
                    self.card_images[card] = 'Cards/11. Strength.png'
                    self.predictions[card] = {
                        "upright": "Strength: Courage and emotional control will lead to success.",
                        "reversed": "Strength (Reversed): Inner doubt or weakness undermines your efforts."
                    }
                case 12:
                    self.card_images[card] = 'Cards/12. The Hanged Man.png'
                    self.predictions[card] = {
                        "upright": "The Hanged Man: Sacrifice and patience are necessary to move forward.",
                        "reversed": "The Hanged Man (Reversed): Stagnation or resistance to letting go."
                    }
                case 13:
                    self.card_images[card] = 'Cards/13. Death.png'
                    self.predictions[card] = {
                        "upright": "Death: Deep transformation, end of a cycle and beginning of another.",
                        "reversed": "Death (Reversed): Resistance to change delays transformation."
                    }
                case 14:
                    self.card_images[card] = 'Cards/14. Temperance.png'
                    self.predictions[card] = {
                        "upright": "Temperance: Balance and harmony in your actions and decisions.",
                        "reversed": "Temperance (Reversed): Imbalance or excess disrupts your peace."
                    }
                case 15:
                    self.card_images[card] = 'Cards/15. The Devil.png'
                    self.predictions[card] = {
                        "upright": "The Devil: Temptations and material attachments may be holding you back.",
                        "reversed": "The Devil (Reversed): Breaking free from chains or negative patterns."
                    }
                case 16:
                    self.card_images[card] = 'Cards/16. The Star.png'
                    self.predictions[card] = {
                        "upright": "The Star: Hope and spiritual guidance light your path.",
                        "reversed": "The Star (Reversed): Loss of faith or dimming hope."
                    }
                case 17:
                    self.card_images[card] = 'Cards/17. The Tower.png'
                    self.predictions[card] = {
                        "upright": "The Tower: Drastic changes and unexpected revelations.",
                        "reversed": "The Tower (Reversed): Avoiding necessary upheaval delays growth."
                    }
                case 18:
                    self.card_images[card] = 'Cards/18. The Moon.png'
                    self.predictions[card] = {
                        "upright": "The Moon: Confusion and illusions, trust your intuition to clarify.",
                        "reversed": "The Moon (Reversed): Clarity emerges, illusions dissipate."
                    }
                case 19:
                    self.card_images[card] = 'Cards/19. The Sun.png'
                    self.predictions[card] = {
                        "upright": "The Sun: Success, clarity, and happiness are on your way.",
                        "reversed": "The Sun (Reversed): Temporary setbacks cloud your joy."
                    }
                case 20:
                    self.card_images[card] = 'Cards/20. Judgement.png'
                    self.predictions[card] = {
                        "upright": "Judgement: Reflection and renewal, it's time to make important decisions.",
                        "reversed": "Judgement (Reversed): Self-doubt or avoidance delays your awakening."
                    }
                case 21:
                    self.card_images[card] = 'Cards/21. The World.png'
                    self.predictions[card] = {
                        "upright": "The World: Completion and success, you have achieved a great milestone.",
                        "reversed": "The World (Reversed): Incomplete cycles or lack of closure."
                    }

    def shuffle(self):
        """Shuffle the deck of cards."""
        random.shuffle(self.cards)

    def select_card(self):
        """Select and remove a random card from the deck, returning (card, is_reversed)."""
        if not self.cards:  # Si el mazo está vacío, reiniciarlo
            self.cards = self.original_cards.copy()
            self.shuffle()
        card = random.choice(self.cards)
        self.cards.remove(card)  # Eliminar la carta seleccionada del mazo
        is_reversed = random.choice([True, False])  # 50% de probabilidad de estar invertida
        return (card, is_reversed)

    def get_img(self, card):
        """Return the image path for the given card (ignoring reversed state for now)."""
        if isinstance(card, tuple):  # Si se pasa una tupla (card, is_reversed)
            card = card[0]  # Usar solo el número de la carta
        return self.card_images.get(card, None)

    def get_pred(self, card):
        """Return the prediction for the given card, considering if it's reversed."""
        if isinstance(card, tuple):  # Si se pasa una tupla (card, is_reversed)
            card_num, is_reversed = card
            predictions = self.predictions.get(card_num, {"upright": "No prediction available.", "reversed": "No prediction available."})
            return predictions["reversed"] if is_reversed else predictions["upright"]
        return "No prediction available."  # Fallback si no se pasa una tupla válida

    def reset_deck(self):
        """Reset the deck to its original state and shuffle."""
        self.cards = self.original_cards.copy()
        self.shuffle()