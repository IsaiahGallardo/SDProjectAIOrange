import numpy as np

from PIL import Image
import PIL

def gen_report_text(avg_vertical_breaks):
   report_text = ""
   for key, avg_vertical_break in avg_vertical_breaks.items():
        name, pitches = key
        report_text += f"Pitcher: {name}, Pitch Type: {pitches}, Average Vertical Break: {avg_vertical_break}\n"
        return report_text

def gen_report_images():
    pass

# takes the dataframe as the parameter in order to split the data by pitcher and later
# by pitch type
def gen_report_data(df):
    avg_vertical_breaks = {}
    # loops through each unique pitcher
    names = df['Pitcher'].unique()
    for name in names:
        # creates new dataset
        name_df = df[df['Pitcher'] == name]

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
        pitch_type = name_df[('TaggedPitchType')].unique()
        for pitches in pitch_type:
            # creates new dataset
            pitch_df = name_df[name_df['TaggedPitchType'] == pitches]

            avg_vertical_break = np.mean(pitch_df['VertBreak'])
            avg_vertical_breaks[(name, pitches)] = avg_vertical_break

            # gets pitch specific text output and saves to text file corresponding to their name and pitch
            text_output_pitch = gen_report_text(avg_vertical_breaks)
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
