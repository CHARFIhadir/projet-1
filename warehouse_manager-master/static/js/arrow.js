/* this function targets a class assocaited with the product table header elements. It toggles a class designed to 
create a small triangle to simulate sorting through the sort function. The class swap changes the orientation
from facing down, to up, depending on whcih sort function is in play.
 */

function arrow(n) {
  var element = document.getElementById("productsTable");
  element.getElementsByTagName("TH")[n].classList.toggle("headerSortUp");
  element.getElementsByTagName("TH")[n].classList.toggle("headerSortDown");
} 