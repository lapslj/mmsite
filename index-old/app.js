function setTimeBasedTheme() {
    const hour = new Date().getHours();
    const container = document.body;
    
    // Remove any existing theme classes
    container.classList.remove('morning', 'afternoon', 'evening', 'night');
    
    // Add appropriate theme class based on time
    if (hour >= 5 && hour < 12) {
      container.classList.add('morning');
    } else if (hour >= 12 && hour < 17) {
      container.classList.add('afternoon');
    } else if (hour >= 17 && hour < 20) {
      container.classList.add('evening');
    } else {
      container.classList.add('night');
    }
  }
  
  // Run when page loads
  setTimeBasedTheme();
  
  // Optionally check every minute for time changes
  setInterval(setTimeBasedTheme, 60000);