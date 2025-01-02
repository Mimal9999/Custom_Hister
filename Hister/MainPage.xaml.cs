using CommunityToolkit.Maui.Core.Primitives;
using CommunityToolkit.Maui.Views;
using MediaManager;
using System.ComponentModel;
using System.Diagnostics;
using YoutubeExplode;
using YoutubeExplode.Videos;
using YoutubeExplode.Videos.Streams;
using ZXing.Net.Maui;
using ZXing.Net.Maui.Controls;

namespace Hister;

public partial class MainPage : ContentPage
{
    private CameraBarcodeReaderView _cameraBarcodeReaderView;

    public MainPage()
    {
        InitializeComponent();
        AudioPlayer.PropertyChanged += MediaElement_PropertyChanged;

        _cameraBarcodeReaderView = new CameraBarcodeReaderView
        {            
            HorizontalOptions = LayoutOptions.FillAndExpand,
            VerticalOptions = LayoutOptions.FillAndExpand,
        };

        _cameraBarcodeReaderView.BarcodesDetected += OnBarcodesDetected;

        QRCodeGrid.Children.Add(_cameraBarcodeReaderView);
    }   
    private void MediaElement_PropertyChanged(object? sender, PropertyChangedEventArgs e)
    {
        if (e.PropertyName == MediaElement.DurationProperty.PropertyName)
        {
            PlaybackSlider.Maximum = AudioPlayer.Duration.TotalSeconds;
        }
    }

    /// <summary>
    /// Handles barcode detection events. If a detected barcode contains a YouTube link, 
    /// it processes the link, fetches the corresponding audio, and starts playing it. 
    /// Displays appropriate messages to the user during the process.
    /// </summary>
    /// <param name="sender">The source of the event.</param>
    /// <param name="e">The event arguments containing the barcode results.</param>
    private async void OnBarcodesDetected(object sender, ZXing.Net.Maui.BarcodeDetectionEventArgs e)
    {
        // Check if the event arguments or results are null to avoid null reference exceptions
        if (e == null || e.Results == null)
            return;

        try
        {
            // Extract the first detected barcode value
            var detectedCode = e.Results.FirstOrDefault()?.Value;

            if (!string.IsNullOrEmpty(detectedCode) && detectedCode.Contains("youtube.com"))
            {
                // Pause further detection while processing the current code
                _cameraBarcodeReaderView.IsDetecting = false;

                // Ensure UI operations are executed on the main thread
                await MainThread.InvokeOnMainThreadAsync(async () =>
                {
                    await DisplayAlert("Code scanned", $"Content: {detectedCode}", "OK"); //Coment if not needed

                    // Update layout
                    SetControlsVisibility(true);
                    ResultLabel.Text = $"Playing: {detectedCode}";
                    QRCodeGrid.IsVisible = false;

                    // Retrieve the audio URL associated with the YouTube link
                    var audioUrl = await GetYouTubeAudioUrl(detectedCode);

                    if (!string.IsNullOrEmpty(audioUrl))
                    {
                        AudioPlayer.Source = new Uri(audioUrl);

                        // Wait until the media element finishes buffering
                        while (AudioPlayer.CurrentState == CommunityToolkit.Maui.Core.Primitives.MediaElementState.Buffering)
                        {
                            await Task.Delay(100); // Delay to avoid busy waiting
                        }

                        // Start playback
                        PlayMedia();
                    }
                    else
                    {
                        ResultLabel.Text = "Cannot load audio.";
                    }
                });
            }
        }
        catch (Exception ex)
        {
            // Handle any exceptions and display an error message to the user
            await MainThread.InvokeOnMainThreadAsync(async () =>
            {
                await DisplayAlert("Error", $"An error occurred: {ex.Message}", "OK");
            });
        }
    }
    /// <summary>
    /// Starts media playback, enables the playback slider, and updates the Play/Pause button text.
    /// </summary>
    private void PlayMedia()
    {
        PlaybackSlider.IsEnabled = true;
        PlayPauseButton.Text = "Pause";
        AudioPlayer.Play();
    }
    /// <summary>
    /// Sets the visibility of media control elements based on the specified state.
    /// </summary>
    /// <param name="isVisible">A boolean value indicating whether the controls should be visible.</param>
    private void SetControlsVisibility(bool isVisible)
    {
        StopButton.IsVisible = isVisible;
        PlayPauseButton.IsVisible = isVisible;
        PlaybackSlider.IsVisible = isVisible;
        CurrentTimeLabel.IsVisible = isVisible;
        DurationLabel.IsVisible = isVisible;
        scanAgainButton.IsVisible = isVisible;
    }
    /// <summary>
    /// Retrieves the audio URL with the highest bitrate from a given YouTube video URL.
    /// </summary>
    /// <param name="youtubeUrl">The URL of the YouTube video.</param>
    /// <returns>
    /// A task that represents the asynchronous operation. 
    /// The task result contains the URL of the audio stream, or null if an error occurs or no audio stream is available.
    /// </returns>
    private async Task<string?> GetYouTubeAudioUrl(string youtubeUrl)
    {
        var youtube = new YoutubeClient();

        // Try parsing the provided YouTube URL to extract the video ID
        var videoId = VideoId.TryParse(youtubeUrl);

        if (videoId == null) return null;

        try
        {
            // Retrieve the stream manifest asynchronously
            var streamManifest = await Task.Run(async () =>
            {
                return await youtube.Videos.Streams.GetManifestAsync(videoId.Value);
            });

            if (streamManifest == null)
            {
                // Log error and return null if the manifest could not be retrieved
                Console.WriteLine("Error: Unable to retrieve stream manifest.");
                return null;
            }

            Console.WriteLine("Downloading audio");

            // Get the audio stream with the highest bitrate
            var audioStreamInfo = streamManifest.GetAudioStreams().GetWithHighestBitrate();

            if (audioStreamInfo == null)
            {
                // Log error and return null if no audio stream is found
                Console.WriteLine("Error: No audio stream available.");
                return null;
            }

            // Return the URL of the audio stream as a string
            return audioStreamInfo.Url.ToString();
        }
        catch (Exception ex)
        {
            // Log the exception details and return null
            Console.WriteLine($"Error: {ex.Message}");
            return null;
        }
    }
    /// <summary>
    /// Handles the "Scan Again" button click event. 
    /// Stops any ongoing audio playback, resets the audio player, and re-enables barcode detection for scanning.
    /// </summary>
    /// <param name="sender">The source of the event.</param>
    /// <param name="e">The event arguments.</param>
    private void OnScanAgainClicked(object sender, EventArgs e)
    {
        // Stop the audio player and clear the audio source
        AudioPlayer.Stop();
        AudioPlayer.Source = null;

        // Re-enable barcode detection and reset UI elements on the main thread
        MainThread.BeginInvokeOnMainThread(() =>
        {
            _cameraBarcodeReaderView.IsDetecting = true;
            SetControlsVisibility(false);
            QRCodeGrid.IsVisible = true;
        });

        ResultLabel.Text = "Scan QR Code";
    }
    /// <summary>
    /// Handles the "Play/Pause" button click event. 
    /// Toggles the audio playback state and updates the button text accordingly.
    /// </summary>
    /// <param name="sender">The source of the event.</param>
    /// <param name="e">The event arguments.</param>
    private void OnPlayPauseClicked(object sender, EventArgs e)
    {
        // Check the current state of the audio player
        if (AudioPlayer.CurrentState == CommunityToolkit.Maui.Core.Primitives.MediaElementState.Playing)
        {
            AudioPlayer.Pause();
            PlayPauseButton.Text = "Play";
        }
        else
        {
            AudioPlayer.Play();
            PlayPauseButton.Text = "Pause";
        }
    }
    /// <summary>
    /// Handles the "Stop" button click event. 
    /// Stops the audio playback and resets the Play/Pause button text.
    /// </summary>
    /// <param name="sender">The source of the event.</param>
    /// <param name="e">The event arguments.</param>
    private void OnStopClicked(object sender, EventArgs e)
    {
        AudioPlayer.Stop();
        PlayPauseButton.Text = "Play";
    }
    /// <summary>
    /// Updates the playback slider position when the media position changes.
    /// </summary>
    /// <param name="sender">The source of the event (e.g., the audio player).</param>
    /// <param name="e">Event arguments containing the new media position.</param>
    private void OnPositionChanged(object? sender, MediaPositionChangedEventArgs e)
    {
        // Update the slider value to reflect the current playback position
        PlaybackSlider.Value = e.Position.TotalSeconds;
    }

    /// <summary>
    /// Pauses the audio player when the user starts dragging the slider to adjust the playback position.
    /// </summary>
    /// <param name="sender">The source of the event (e.g., the slider).</param>
    /// <param name="e">The event arguments.</param>
    private void Slider_DragStarted(object sender, EventArgs e)
    {
        // Pause the audio player to avoid conflicts while adjusting playback position
        AudioPlayer.Pause();
    }

    /// <summary>
    /// Seeks to the new playback position when the user finishes dragging the slider and resumes playback.
    /// </summary>
    /// <param name="sender">The source of the event (e.g., the slider).</param>
    /// <param name="e">The event arguments.</param>
    private async void Slider_DragCompleted(object? sender, EventArgs e)
    {
        // Ensure the sender is not null; throw an exception if it is
        ArgumentNullException.ThrowIfNull(sender);

        // Get the new slider value, which represents the desired playback position in seconds
        var newValue = ((Slider)sender).Value;

        // Seek to the specified position in the media
        await AudioPlayer.SeekTo(TimeSpan.FromSeconds(newValue), CancellationToken.None);

        // Resume playback after seeking
        AudioPlayer.Play();
    }

}


