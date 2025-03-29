document.addEventListener('DOMContentLoaded', function() {
  const card = document.getElementById('card');
  const successMessage = document.getElementById('success');
  
  // Simple click handler to fade the card
  card.addEventListener('click', function() {
      // Fade out the card
      card.style.transition = 'opacity 1s ease-in';
      card.style.opacity = '0';
      
      // Show success message after animation
      setTimeout(() => {
          successMessage.style.display = 'block';
          card.style.display = 'none';
      }, 1000);

        // Navigate after delay
    setTimeout(function() {
        window.location.href = 'home.html';
      }, 1500);
  });
  
  // For touch devices
  card.addEventListener('touchstart', function(e) {
      e.preventDefault(); // Prevent default touch behavior
  });
  
  card.addEventListener('touchend', function(e) {
      e.preventDefault();
      // Trigger the same animation as click
      card.style.transition = 'opacity 1s ease-in';
      card.style.opacity = '0';
      
      setTimeout(() => {
          successMessage.style.display = 'block';
          card.style.display = 'none';
      }, 1000);

    // Navigate after delay
    setTimeout(function() {
        window.location.href = 'home.html';
      }, 1500);
  });
});
