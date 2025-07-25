
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Summarizer API Demo</title>
  <style>
    body { font-family: sans-serif; padding: 2em; line-height: 1.6; }
    #summary { margin-top: 2em; padding: 1em; background: #f0f8ff; border-left: 4px solid #007acc; }
    button { padding: 0.5em 1em; font-size: 1em; }
  </style>
</head>
<body>
  <h1>🌍 Climate Change and Its Global Impact</h1>
  <p id="article">
    Climate change refers to long-term shifts in temperatures and weather
    patterns, primarily caused by human activities such as burning fossil fuels.
    These changes are not just environmental—they affect economies, health
    systems, agriculture, and even geopolitical stability. Rising sea levels
    threaten coastal cities, while extreme weather events like hurricanes,
    droughts, and wildfires are becoming more frequent and intense. Developing
    nations, often the least responsible for emissions, are disproportionately
    affected. Scientists emphasize the urgency of reducing greenhouse gas
    emissions and transitioning to renewable energy sources. International
    cooperation, policy reform, and technological innovation are key to
    mitigating the worst effects. Public awareness and behavioral change also
    play a crucial role in shaping a sustainable future.
  </p>

  <button id="summarizeBtn">🧠 Summarize This</button>

  <div id="summary"><em>Summary will appear here...</em></div>

  <script>
    document.getElementById('summarizeBtn').addEventListener('click', async () => {
      const text = document.getElementById('article').textContent;
      const summaryBox = document.getElementById('summary');
      summaryBox.textContent = '⏳ Summarizing...';

      if (!('Summarizer' in self)) {
        summaryBox.textContent = '❌ Summarizer API not supported in this browser.';
        return;
      }

      const availability = await Summarizer.availability();
      if (availability === 'unavailable') {
        summaryBox.textContent = '❌ Summarizer model is unavailable.';
        return;
      }

      const summarizer = await Summarizer.create({
        type: 'tldr',
        length: 'medium',
        format: 'plain-text',
        sharedContext: 'This is an educational article about climate change.',
        monitor(monitor) {
          monitor.addEventListener('downloadprogress', (e) => {
            console.log(`Download progress: ${(e.loaded * 100).toFixed(2)}%`);
          });
        }
      });

      await summarizer.ready;

      try {
        const summary = await summarizer.summarize(text);
        summaryBox.textContent = `✅ Summary:\n${summary}`;
      } catch (err) {
        summaryBox.textContent = `⚠️ Error: ${err.message}`;
      }

      summarizer.destroy();
    });
  </script>
</body>
</html>
