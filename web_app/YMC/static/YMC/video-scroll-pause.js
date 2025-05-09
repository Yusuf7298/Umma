document.addEventListener('DOMContentLoaded', function() {
    const videos = document.querySelectorAll('video');
    function pauseAllVideos() {
      videos.forEach(video => {
        video.pause();
      });
    }
    function resumeVideos(){
      videos.forEach(video => {
        if (video.isPlaying){
          video.play()
        }
      })
    }
    document.addEventListener("visibilitychange", function() {
      if (document.hidden) {
        pauseAllVideos();
      } else {
      }
    });
    videos.forEach(video => {
      video.addEventListener('play', function() {
        this.isPlaying = true;
      });
      video.addEventListener('pause', function() {
        this.isPlaying = false;
      });
    });
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.play();
        } else {
          entry.target.pause();
        }
      });
    }, { threshold: 0.5 }); 
    videos.forEach(video => {
      observer.observe(video);
    });
  });
  
  