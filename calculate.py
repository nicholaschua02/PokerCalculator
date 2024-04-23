import itertools

# Ranks and suits in a deck of cards
ranks = '23456789TJQKA'
suits = 'shdc'

# Create a deck of cards
deck = [rank + suit for rank in ranks for suit in suits]

def hand_rank(hand):
    "Evaluate the rank of the best five-card hand from any given set of cards."
    # hand = ["Ts", "Ks", "2s", "2d", "2h"]

    best_rank = None
    for combo in itertools.combinations(hand, 5):
        ranks = ''.join(sorted((rank for rank, suit in combo), reverse=True, key=lambda x: '23456789TJQKA'.index(x)))
        suits = {suit for rank, suit in combo}
        flush = len(suits) == 1
        straight = any(ranks[i:i+5] in 'A23456789TJQKA2345' for i in range(len(ranks) - 4))

        rank_counts = {r: ranks.count(r) for r in ranks}
        groups = sorted(rank_counts.items(), key=lambda x:x[1], reverse=True)
        rank_sorted, counts = zip(*groups)
        rank_sorted = ''.join(rank_sorted)
        
        score = (
            8 if straight and flush else
            7 if counts == (4, 1) else
            6 if counts == (3, 2) else
            5 if flush else
            4 if straight else
            3 if counts == (3, 1, 1) else
            2 if counts == (2, 2, 1) else
            1 if counts == (2, 1, 1, 1) else
            0
        )
        
        rank_order = '23456789TJQKA'

        try:
            rank_result = (score, ranks)
            if rank_result == None:
                best_rank = rank_result
            else:
                if rank_result[0] > best_rank[0]:
                    best_rank = rank_result
                elif rank_result[0] == best_rank[0]:
                    for i in range(5):
                        if rank_order.index(rank_result[1][i]) > rank_order.index(best_rank[1][i]):
                            best_rank = rank_result
                            break
                        elif rank_order.index(rank_result[1][i]) < rank_order.index(best_rank[1][i]):
                            break
        except:
            best_rank = rank_result
    return best_rank

def poker_odds(player_hand, community_cards=[]):
    if not len(community_cards) in (0, 3, 4, 5):
        community_cards = []
    "Calculate the odds of a player's hand winning against all possible hands."
    # Generate remaining deck and possible opponents' hands
    remaining_deck = [card for card in deck if card not in player_hand and card not in community_cards]
    opponent_hands = itertools.combinations(remaining_deck, 2)
    ranks = '23456789TJQKA'

    total = 0
    wins = 0
    draws = 0
    
    losing_hands = []
    
    for hand in opponent_hands:        
        our_hand_wins = 0
        opponent_hand_wins = 0
        mini_draws = 0

        total += 1

        if len(community_cards) == 0:
            total_community = itertools.combinations(remaining_deck, 5)
            for combination in total_community:
                if len(set(combination) & set(hand)) == 0:
                    full_opponent_hand = list(hand) + list(combination)
                    full_player_hand = player_hand + list(combination)
                    player_score = hand_rank(full_player_hand)
                    opponent_score = hand_rank(full_opponent_hand)

                    if player_score > opponent_score:
                        our_hand_wins += 1
                    else:
                        opponent_hand_wins += 1

            if our_hand_wins < opponent_hand_wins:
                print(hand, "LOSS", our_hand_wins / (our_hand_wins + opponent_hand_wins))
            else:
                wins += 1

        if len(community_cards) == 3:
            extra_community = itertools.combinations(remaining_deck, 2)
            for combination in extra_community:
                if len(set(combination) & set(hand)) == 0:
                    total_community = list(combination) + community_cards
                    full_opponent_hand = list(hand) + total_community
                    full_player_hand = player_hand + total_community
                    player_score = hand_rank(full_player_hand)
                    opponent_score = hand_rank(full_opponent_hand)
                    if player_score[0] > opponent_score[0]:
                        our_hand_wins += 1
                    elif player_score[0] < opponent_score[0]:
                        opponent_hand_wins += 1
                    else:
                        for i in range(5):
                            if ranks.index(player_score[1][i]) > ranks.index(opponent_score[1][i]):
                                our_hand_wins += 1
                                break
                            elif ranks.index(player_score[1][i]) < ranks.index(opponent_score[1][i]):
                                opponent_hand_wins += 1
                                break

            if our_hand_wins < opponent_hand_wins:
                x = 0
                # print(hand, "LOSS", our_hand_wins / (our_hand_wins + opponent_hand_wins))
            elif our_hand_wins == opponent_hand_wins:
                draws += 1
            else:
                wins += 1

        if len(community_cards) == 4:
            extra_community = itertools.combinations(remaining_deck, 1)
            for combination in extra_community:
                if len(set(combination) & set(hand)) == 0:
                    total_community = list(combination) + community_cards
                    full_opponent_hand = list(hand) + total_community
                    full_player_hand = player_hand + total_community
                    player_score = hand_rank(full_player_hand)
                    opponent_score = hand_rank(full_opponent_hand)
                    if player_score[0] > opponent_score[0]:
                        our_hand_wins += 1
                    elif player_score[0] < opponent_score[0]:
                        opponent_hand_wins += 1
                    else:
                        for i in range(5):
                            if ranks.index(player_score[1][i]) > ranks.index(opponent_score[1][i]):
                                our_hand_wins += 1
                                break
                            elif ranks.index(player_score[1][i]) < ranks.index(opponent_score[1][i]):
                                opponent_hand_wins += 1
                                break

            if our_hand_wins < opponent_hand_wins:
                x = 0
                # print(hand, "LOSS", our_hand_wins / (our_hand_wins + opponent_hand_wins))
            elif our_hand_wins == opponent_hand_wins:
                draws += 1
            else:
                wins += 1

        if len(community_cards) == 5:
            draw = False
            full_opponent_hand = list(hand) + community_cards
            full_player_hand = player_hand + community_cards
            player_score = hand_rank(full_player_hand)
            opponent_score = hand_rank(full_opponent_hand)

            if player_score[0] > opponent_score[0]:
                wins += 1
            elif player_score[0] == opponent_score[0]:
                draw = True
                for i in range(5):
                    if ranks.index(player_score[1][i]) > ranks.index(opponent_score[1][i]):
                        wins += 1
                        draw = False
                        break
                    elif ranks.index(player_score[1][i]) < ranks.index(opponent_score[1][i]):
                        draw = False
                        break
                if draw:
                    draws += 1

    return wins, draws, total

# Example usage
player_hand = input("Input Player Hand: ").split(" ") # ['As', 'Ks']  # Ace and King of spades
community_cards = input("Input Community Cards: ").split(" ") # ['2s', '2d', '2h', '2c', '3s']  # Three community cards

player_hand = ['As', 'Ks']
community_cards = ['2s', '2d', '2h', '2c', '3s']

wins, draws, total = poker_odds(player_hand, community_cards)

print(f"\nChance of winning: {wins/total * 100:.2f}%")
print(f"\nChance of drawing: {draws/total * 100:.2f}%")
print(f"\nChance of losing: {(total - wins - draws)/total * 100:.2f}%")