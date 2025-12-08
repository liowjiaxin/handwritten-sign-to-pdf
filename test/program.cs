using System;
using System.IO;
using OpenCvSharp;
using iText.Kernel.Pdf;
using iText.Layout;
using iText.Layout.Element;
using iText.IO.Image;

class Program
{
    static void Main()
    {
        // Use the directory where you are running the terminal command
        string root = Environment.CurrentDirectory;
        
        string signImage = Path.Combine(root, "sign.jpg");
        string transSig = Path.Combine(root, "transparent_sig.png");
        string pdfIn = Path.Combine(root, "dangerous_goods_form.pdf");
        string pdfOut = Path.Combine(root, "signed_dangerous_goods_form.pdf");

        try 
        {
            Console.WriteLine($"📂 Current Folder: {root}");
            
            Console.WriteLine("🚀 Processing signature...");
            ExtractSignature(signImage, transSig);

            Console.WriteLine("🚀 Signing PDF...");
            InsertSignature(pdfIn, transSig, pdfOut);

            Console.WriteLine($"✅ Done! Saved to: {pdfOut}");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"❌ Error: {ex.Message}");
        }
    }

    static void ExtractSignature(string input, string output)
    {
        if (!File.Exists(input)) throw new FileNotFoundException($"Cannot find: {input}");
        
        using var img = Cv2.ImRead(input);
        using var gray = new Mat();
        using var blur = new Mat();
        using var thresh = new Mat();

        Cv2.CvtColor(img, gray, ColorConversionCodes.BGR2GRAY);
        Cv2.GaussianBlur(gray, blur, new Size(5, 5), 0);
        Cv2.AdaptiveThreshold(blur, thresh, 255, AdaptiveThresholdTypes.GaussianC, ThresholdTypes.BinaryInv, 15, 8);

        using var bgra = new Mat();
        Cv2.CvtColor(img, bgra, ColorConversionCodes.BGR2BGRA);
        Mat[] ch = Cv2.Split(bgra);
        ch[3] = thresh; 
        Cv2.Merge(ch, bgra);
        bgra.SaveImage(output);
    }

    static void InsertSignature(string input, string sigImg, string output)
    {
        if (!File.Exists(input)) throw new FileNotFoundException($"Cannot find: {input}");

        using var reader = new PdfReader(input);
        using var writer = new PdfWriter(output);
        using var pdfDoc = new PdfDocument(reader, writer);
        var document = new Document(pdfDoc);

        ImageData data = ImageDataFactory.Create(sigImg);
        Image img = new Image(data).SetWidth(150f);

        var page = pdfDoc.GetFirstPage().GetPageSize();
        // Position at bottom right with some margin
        img.SetFixedPosition(page.GetWidth() - 200f, 50f);
        img.SetFixedPosition(page.GetWidth() - 200f, 10f);

        document.Add(img);
        document.Close();
    }
}