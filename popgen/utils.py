
import pathlib
import scipy.special
import os




def norm_cdf(x):
    """Faster than scipy.stats.norm.cdf
    https://en.wikipedia.org.wiki/Normal_distribution
    """
    return 0.5*(1 + scipy.special.erf(x/np.sqrt(2)))

def get_ugali_dir():
    """Get the path to the ugali data directory from the environment"""

    dirname = os.getenv('UGALIDIR')

    # Get the HOME directory
    if not dirname:
        dirname=os.path.join(os.getenv('HOME'),'.ugali')

    if not os.path.exists(dirname):
        from logger import logger
        msg = "Creating UGALIDIR:\n%s"%dirname
        logger.warning(msg)
    ugaliPath=pathlib.Path(dirname)

    ugaliPath.mkdir(parents=True, exist_ok=True)
    return ugaliPath

def get_iso_dir():
    """Get the ugali isochrone directory."""
    dirname = os.path.join(get_ugali_dir(),'isochrones')

    if not os.path.exists(dirname):
        from logger import logger
        msg = "Isochrone directory not found:\n%s"%dirname
        logger.warning(msg)

    return dirname

def distanceToDistanceModulus(distance):
    """ Return distance modulus for a given distance (kpc).

    Parameters
    ----------
    distance : distance (kpc)

    Returns
    -------
    mod : distance modulus
    """
    return 5. * (np.log10(np.array(distance)) + 2.)

dist2mod = distanceToDistanceModulus

def distanceModulusToDistance(distance_modulus):
    """ Return distance (kpc) for a given distance modulus.

    Parameters
    ----------
    distance_modulus : distance modulus

    Returns
    -------
    distance : distance (kpc)
    """
    return 10**((0.2 * np.array(distance_modulus)) - 2.)

mod2dist = distanceModulusToDistance


def sum_mags(mags, weights=None):
    """
    Sum an array of magnitudes in flux space.

    Parameters:
    -----------
    mags    : array of magnitudes
    weights : array of weights for each magnitude (i.e. from a pdf)

    Returns:
    --------
    sum_mag : the summed magnitude of all the stars
    """
    flux = 10**(-np.asarray(mags) / 2.5)
    if weights is None:
        return -2.5 * np.log10(np.sum(flux))
    else:
        return -2.5 * np.log10(np.sum(weights*flux))