function setTimeBasedTheme() {
    const hour = new Date().getHours();
    const body = document.body;
    
    // Remove any existing theme classes
    // body.classList.remove('morning', 'afternoon', 'evening', 'night');
    
    // Add appropriate theme class based on time
    if (hour >= 5 && hour < 12) {
      body.classList.add('morning');
    } else if (hour >= 12 && hour < 17) {
      body.classList.add('afternoon');
    } else if (hour >= 17 && hour < 20) {
      body.classList.add('evening');
    } else {
      body.classList.add('night');
    }
  }
  
  // Run when page loads
  setTimeBasedTheme();
  
  // Optionally check every minute for time changes
  setInterval(setTimeBasedTheme, 60000);