#' Load a single RCA or proximity file. These files were orignially
#' saved as a .csv file contianing a matrix, with a row for each
#' country and a column for each discipline
#'
#' @export
#'
#' @param path.to.file Path to the RCA or proximity file to load. The file
#' should be formatted as a matrix, such that the first column are the names
#' of countries, and each column is the name of a discipline
#' @param type A string representing whether the file contains an RCA, or a
#' Proximity data
#'
#' @return A dataframe containing the RCA/proximity meausre mapped to each
#' country, disicpline, and year interval
#'
#' @importFrom dplyr %>%
#' @importFrom tidyr gather
#'
LoadFile <- function(path.to.file, type = NULL) {
  # Supress warnings for this one command, as one column name is missing and
  # loaded with a default name, resulting in a warning that we can
  # safely ignore
  options(warn=-1)
  # First, load the file. It should be of type csv
  loaded.data = readr::read_csv(path.to.file, col_types = readr::cols())

  # Turn wanrings back on
  options(warn=0)

  if ("X1" %in% names(loaded.data)) {
    loaded.data <- loaded.data %>% select(-X1)
  }

  # Next, exract the start and end of the year intervals
  # from the filename of the file. These should be ordered,
  # each year represented as a 4-digit number, i.e. 2018
  filename <- dplyr::last(unlist(strsplit(path.to.file, "/")))
  year.start = substr(filename, 1, 4)
  year.end = substr(filename, 5, 8)

  # Apply a default value to the "type" variable
  if (is.null(type)) {
    type = ""
  }

  # Check either the provided type, or the name of the file.
  # If the type is an RCA file, then gather with the appropriate variable name
  if (tolower(type) == "rca" | grepl("rca.", filename, ignore.case = T)) {
    loaded.data <- loaded.data %>%
      tidyr::gather(Specialty, RCA, -COUNTRY) %>%
      dplyr::rename(Country = COUNTRY)
  } else if (grepl("prox", type, ignore.case = T) |
             grepl("prox", filename, ignore.case = T)) {
    # If the file is of type "proximity", gather with correct name
    loaded.data <- loaded.data %>%
      tidyr::gather(Specialty, Proximity)
      #dplyr::rename(Specialty.x = X1, Specialty.y = Specialty)
  } else {
    stop(sprintf("Warning: type %s is not defined", type))
  }

  # Provide a start and end year to the intervels
  loaded.data <- loaded.data %>%
    dplyr::mutate(Years = paste0(year.start, "-", year.end))

  # Return the data
  return(loaded.data)
}
