import powerlaw

from DataReader import TableReader

import matplotlib.pyplot as plt

if __name__ == '__main__':
    estimate_dir = "/home/valentin/Desktop/Thesis II/Zipf Error/Estimates"
    lang = "NO"
    estimate_file = lang+"_ToktokTokenizer_ArticleSplitter"
    reader = TableReader(estimate_dir+"/"+estimate_file, [str, int, int])
    data = reader.read_data()

    counts = data["count"]

    pos_counts = [c for c in counts if c > 0]

    print(counts[:10])

    print(min(counts))

    powerlaw.plot_cdf(counts)
    # plt.show()

    powerlaw.plot_pdf(pos_counts)
    # plt.show()

    fitted_dist = powerlaw.Fit(pos_counts, discrete=True)

    for key, val in fitted_dist.__dict__.items():
        print(key, ":\t", val if hasattr(val, "__len__") and len(val) < 100 else "val too long")
        print()




    print("\n\n", fitted_dist.find_xmin())
