/* BlackJackDavey
 *
 * A entry for
 * http://codegolf.stackexchange.com/questions/2698/a-blackjack-koth-contest
 * copyright 2011 
 *
 * Currently expects a slightly extended version of the spec. Two
 * expected changes:
 * - Tens will be represented as 'T'
 * - The visible card string will include '#' for those cards whose
 *     *backs* we can see (slight improvement in card counting technique)
 * 
 * No disaster if neither feature is present, just sligtly degraded
 * performance.
 */
#include <stdio.h>
#include <string.h>

/* A full deck has a total value of 4*( (11*5) + (3*10) + ace ) where
 * ace is 11 or according to our need.
 **/
int fullWeight(const int current){
  int ace = (current>10) ? 1 : 11;
  return 4 * ( 11*5 + 3*10 + ace);
}
/* Return the value of a particular card in the context of our
 * current score
 */
int cardWeight(const char c, const int current){
 switch (c) {
 case '1': case '2': case '3': case '4': case '5':
 case '6': case '7': case '8': case '9':
   return (c - '0');
 case 'T': case 'J': case 'Q': case 'K':
   return 10;
 case 'A':
   return current>10 ? 1 : 11;
 }
 return 0;
}
/* returns the mean card *value* to be expected from the deck 
 *
 * Works by computing the currently unknown value and diviing by the
 * number of remaining cards 
 */
float weight(const char*known, const int current){
  int weight = fullWeight(current);
  int count=52;
  int uCount=0;
  const char*p=known;
  while (*p != '\0') {
    if (*p == '#') { /* Here '#' is a stand in for the back of a card */
      uCount++;
    } else {
      weight -= cardWeight(*p,current);
    }
    count--;
    p++;
    if ( count==0 && *p != '\0') {
      count += 52;
      weight += fullWeight(current);
    }
  }
  return (1.0 * weight)/(count+uCount);
}


int main(int argc, char*argv[]){
  int score=atoi(argv[1]);
  const char*hand=argv[2];
  const char*visible=argv[3];
  int stake=atoi(argv[4]);
  int chips=atoi(argv[5]);

  /* If current stake is less than 10, bet all the rest because a loss
     does not leave us enough to continue */
  if (chips < 10 && chips > 0) {
    printf("B %d\n",chips);
    return 0;
  }
  /* First round stategy differs from the rest of the game */
  if (strlen(hand)==2 && stake==10) {
    switch(score){
    case 10:
    case 11: /* Double down on particularly strong hands */
      if (chips >= 10) {
    printf("D\n");
    return 0;
      }
      break;
    default:
      break;
    };
  }
  /* In future rounds or when first round spcialls don't apply it is
     all about maximizing chance of getting a high score */
  if ((score + weight(visible,score)) <= 21) {
    /* if the oods are good for getting away with it, hit */
    printf("H\n");
    return 0;
  }
  /* Here odd are we bust if we hit, but if we are too low, the dealer
     probably makes it.*/
  printf("%c\n", score>14 ? 'S' : 'H');
  return 0;
}
