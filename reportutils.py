from PIL import Image
import PIL

def gen_report_text():
   pass


def gen_report_images():
    pass

# takes the dataframe as the parameter in order to split the data by pitcher and later
# by pitch type
def gen_report_data(df):
    # loops through each unique pitcher
    names = df['Pitcher'].unique()
    for name in names:
        # gets (general) text output and saves to text file corresponding to their name
        text_output = gen_report_text()
        f = open(name + ".txt", "w")
        f.write(text_output)
        f.close()
        # gets (general) image output and saves to jpg file corresponding to their name
        image_output = gen_report_images()
        im1 = Image.open(image_output)
        im1 = im1.save(name + ".jpg")
        # loops through all the kinds of pitches for that person
        pitch_type = df[('TaggedPitchType')].unique()
        for pitches in pitch_type:
            # gets pitch specific text output and saves to text file corresponding to their name and pitch
            text_output_pitch = gen_report_text()
            f = open(name + pitches + ".txt", "w")
            f.write(text_output_pitch)
            f.close()
            # gets pitch specific image output and saves to text file corresponding to their name and pitch
            image_output_pitch = gen_report_images()
            im1 = Image.open(image_output_pitch)
            im1.save(name + ".jpg")
            im1.close()
    # these two lines below i am unsure of...
    # what is this function supposed to return? There will be too many images/text files to reference?
    latex_output = report_to_latex()
    return latex_output


def report_to_latex():
    pass
