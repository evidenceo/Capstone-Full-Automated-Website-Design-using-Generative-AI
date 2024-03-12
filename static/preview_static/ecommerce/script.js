function navigateTo(pageName) {
    // Send a message to the parent window
    window.parent.postMessage({ type: 'navigate', pageName: pageName }, '*');
    }
