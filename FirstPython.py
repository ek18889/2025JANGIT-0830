import csv
#adding main lines here.
FILE1 = "file1.csv"
FILE2 = "file2.csv"
OUTPUT = "output.csv"

BUFFER_SIZE = 16 * 1024 * 1024

# Windows-compatible CSV field size limit
try:
    csv.field_size_limit(2**31 - 1)
except OverflowError:
    csv.field_size_limit(1024 * 1024 * 1024)


def compare_csv(file1, file2, output):

    with open(
        file1,
        "r",
        encoding="utf-8",
        newline="",
        buffering=BUFFER_SIZE,
    ) as f1, open(
        file2,
        "r",
        encoding="utf-8",
        newline="",
        buffering=BUFFER_SIZE,
    ) as f2, open(
        output,
        "w",
        encoding="utf-8",
        newline="",
        buffering=BUFFER_SIZE,
    ) as fout:

        reader1 = csv.reader(f1)
        reader2 = csv.reader(f2)

        writer = csv.writer(
            fout,
            lineterminator="\n"
        )

        row_count = 0

        for row_count, (row1, row2) in enumerate(
            zip(reader1, reader2),
            start=1
        ):

            if len(row1) != len(row2):
                raise ValueError(
                    f"Column count mismatch at row {row_count}: "
                    f"{file1}={len(row1)}, "
                    f"{file2}={len(row2)}"
                )

            output_row = []

            for value1, value2 in zip(row1, row2):

                if value1 == value2:
                    output_row.append(value1)
                else:
                    output_row.append(
                        f"[{value1}][{value2}]"
                    )

            writer.writerow(output_row)

            if row_count % 100_000 == 0:
                print(
                    f"Processed {row_count:,} rows...",
                    flush=True
                )

        extra1 = next(reader1, None)
        extra2 = next(reader2, None)

        if extra1 is not None or extra2 is not None:
            raise ValueError(
                "The two CSV files contain different "
                "numbers of rows."
            )

    print(
        f"Completed: {row_count:,} rows "
        f"written to {output}"
    )


if __name__ == "__main__":
    compare_csv(FILE1, FILE2, OUTPUT)
