# 🎥 Crux Crop — Smart Face-Centered Video Cropping

**Crux Crop** is a part of the [Crux](https://essenceai.world) project that **automatically detects and crops the main face** in a video, keeping it centered throughout. It's especially useful for turning horizontal videos into vertical formats for content creation—like **Reels, YouTube Shorts, or TikToks**.

---

<table>
  <tr>
    <th>Original Video</th>
    <th>Cropped Video</th>
  </tr>
  <tr>
    <td>
      <img src="examples/original.gif" width="300"/>
      <br><em>Aspect Ratio: 16:9</em> <!-- Example aspect ratio for the original video -->
    </td>
    <td>
      <img src="examples/output_video.gif" width="300"/>
      <br><em>Aspect Ratio: 9:16</em> <!-- Example aspect ratio for the cropped video -->
    </td>
  </tr>
</table>

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/harshbhatt7585/crux-crop.git
cd crux-crop
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Cropper

```bash
python run.py <video_path> <output_path>
```

You can also customize behavior using optional flags (e.g., crop size, smoothness, etc.). Run \`python run.py --help\` for the full list.

---

## How It Works

Crux Crop processes your input video in the following way:

1. Reads the video frame-by-frame.
2. Detects all faces in each frame using OpenCV's Haar Cascade.
3. Selects the **largest face** (assuming it's the main subject).
4. Calculates a crop box centered around that face.
5. Smooths the crop window horizontally across frames to reduce jitter.
6. Crops and resizes the frame to the desired output size.
7. If **no face is found**, falls back to a centered, letterboxed version of the original frame.

---

## Smoothing Explained

When you crop each frame based on the detected face position, the output video can **jitter** due to small variations between frames.

To fix this, we use a **smoothing technique** controlled by \`--smooth-frames\`:

- It keeps a history of face center positions.
- Then it uses a **moving average** of those positions to smooth out crop locations.
- Higher values (e.g., \`30\`) make transitions smoother but less responsive to sudden face movements.
- Lower values (e.g., \`3\`) are more reactive but may cause jitter.

---

## Known Limitations

- Small jitters can still occur, especially during transitions from **cropped mode to fallback mode** (when a face is no longer detected).
- Currently, it only supports **horizontal panning** and assumes a single primary face.
- It uses a simple Haar Cascade which may miss faces in low light or side profiles.

---

## 🛠️ Contributing

Want to make Crux Crop better?

- ⭐ Star the repo
- Report bugs or issues
- Submit pull requests (CLI improvements, model upgrades, multi-face handling, etc.)
