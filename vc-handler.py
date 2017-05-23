import subprocess
import re

# TODO: Check for optional placeholders
# TODO: handle multi line declaration


# Return the delta between HEAD branch and development branch
def get_delta():
    current_branch = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip()
    development_branch = subprocess.check_output(["git", "rev-parse", "master"]).strip()

    sha_to_compare = development_branch + '..' + current_branch

    print "Executing:  git diff --unified=0 --diff-filter=M " + sha_to_compare + "\n"

    return subprocess.check_output(['git', 'diff', '--unified=0', '--diff-filter=M', sha_to_compare])


# Create list of all translations extracted from, Git branches, delta
def extract_translations_from_delta():
    delta = get_delta()
    print delta
    translations_list = list()

    translations_list.extend(commented_translations(delta))
    translations_list.extend(php_translations(delta))
    translations_list.extend(javascript_translations(delta))

    for line in translations_list:
        print line


# Extract comment prefixed translation/s
def commented_translations(delta):

    re_results = re.findall('(@behalf-translation)(.+)', delta)

    results_list = list()

    for result in re_results:
        # Grab the 2nd group of the match (contains the translation) and split to category and key
        translation = result[1].split('.')
        results_list.append(translation)

    return results_list


# Extract PHP implemented translation/s
def php_translations(delta):

    re_results = re.findall('(_t\()(.*?)\);', delta)

    results_list = list()

    for result in re_results:
        # Clean extracted translation and split to category and key
        translation = re.sub("'", "", result[1]).split(',')
        results_list.append(translation)

    return results_list


# Extract JavaScript implemented translation/s
def javascript_translations(delta):

    re_results = re.findall('(i18next.t\()(.*?)\)', delta)

    results_list = list()

    for result in re_results:
        # Clean extracted translation and split to category and key
        translation = re.sub("'", "", result[1]).split('.')
        results_list.append(translation)

    return results_list


extract_translations_from_delta()
