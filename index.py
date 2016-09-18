import rinobot_plugin as bot
from numpy import *
import sys
import os

DSet2DC1DIBlock = 120
DataSetAbscissaRangeMember = -29838
DataSetIntervalMember = -29836
DataSetNumPointsMember = -29835
DataSetXAxisLabelMember = -29833
DataSetYAxisLabelMember = -29832
DataSetDataMember = -29828
DataSetNameMember = -29827
DataSetAliasMember = -29823

def eof(fd):
    last_pos = fd.tell()

    if fd.read(1) == "":
        return True
    elif len(fromfile(fd, int16, 1)) == 0:
        return True
    else:
        fd.seek(last_pos)
        return False


def loadfile(filepath, verbose=False):
    fd = open(filepath, "rb")
    fname = filepath.split('/')[-1]

    signature = fromfile(fd, dtype="<i1", count=4)
    signature = ''.join(map(chr, list(signature)))

    if signature != "PEPE":
        raise ValueError('Not valid Perkin Elmer file: %s' % signature)
        return False, 0, 0, 0

    try:
        description = fromfile(fd, dtype="<i1", count=40)
        description = ''.join(map(chr, list(description)))

    except ValueError:
        pass
        description = ""

    if verbose:
        print(signature)
        print(description)

    xLen = int(0)

    while not eof(fd):
        blockID = fromfile(fd, int16, 1)[0]
        blockSize = fromfile(fd, int32, 1)[0]

        if blockID == DSet2DC1DIBlock:
            pass

        elif blockID == DataSetAbscissaRangeMember:
            fromfile(fd, int16, 1)
            x0 = fromfile(fd, float64, 1)
            xEnd = fromfile(fd, float64, 1)

        elif blockID == DataSetIntervalMember:
            fromfile(fd, int16, 1)
            xDelta = fromfile(fd, float64, 1)

        elif blockID == DataSetNumPointsMember:
            fromfile(fd, int16, 1)
            xLen = fromfile(fd, int32, 1)

        elif blockID == DataSetXAxisLabelMember:
            fromfile(fd, int16, 1)
            length = fromfile(fd, int16, 1)
            xLabel = fromfile(fd, "<i1", length)
            xLabel = ''.join(map(chr, list(xLabel)))

        elif blockID == DataSetYAxisLabelMember:
            fromfile(fd, int16, 1)
            length = fromfile(fd, int16, 1)
            yLabel = fromfile(fd, "<i1", length)
            yLabel = ''.join(map(chr, list(yLabel)))

        elif blockID == DataSetAliasMember:
            fromfile(fd, int16, 1)
            length = fromfile(fd, int16, 1)
            alias = fromfile(fd, "<i1", length)
            alias = ''.join(map(chr, list(alias)))

        elif blockID == DataSetNameMember:
            fromfile(fd, int16, 1)
            length = fromfile(fd, int16, 1)
            originalName = fromfile(fd, "<i1", length)
            originalName = ''.join(map(chr, list(originalName)))

        elif blockID == DataSetDataMember:
            fromfile(fd, int16, 1)
            length = fromfile(fd, int32, 1)
            if xLen == 0:
                xLen = length / 8
            yData = fromfile(fd, float64, xLen)

        else:
            fd.seek(blockSize, 1)

    xData = arange(x0, xEnd + xDelta, xDelta)

    return xData, yData, xLabel, yLabel


def main():
    filepath = bot.filepath()
    x, y, xL, yL = loadfile(filepath, verbose=False)

    outname = bot.no_extension() + '-sp-converted.txt'
    outpath = bot.output_filepath(outname)

    if x is not False:
        savetxt(outpath, vstack((x, y)).T, fmt="%1.6lf")


if __name__ == "__main__":
    main()
