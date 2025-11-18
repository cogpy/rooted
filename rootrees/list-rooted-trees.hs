{-|
List all rooted trees with n nodes.

This implementation generates unlabeled rooted trees by building them from
partitions of integers. The algorithm works by:
1. Breaking n down into sums of smaller integers (partitions)
2. For each partition, selecting and combining subtrees that match the partition
3. Wrapping the result in parentheses to create a new tree

The trees are represented as strings using nested parentheses notation,
where each pair of parentheses represents a node (bag) and its subtrees.
-}

import System.Environment (getArgs)
import System.Exit (exitFailure)
import System.IO (hPutStrLn, stderr)
import Text.Read (readMaybe)

-- | Break n down into sum of smaller integers (integer partitions)
-- Returns list of partitions, where each partition is a list of (count, value) pairs
parts :: Int -> [[(Int, Int)]]
parts n = f n 1
  where
    f n x
      | n == 0 = [[]]
      | x > n = []
      | otherwise =
        f n (x + 1) ++
        concatMap
          (\c -> map ((c, x) :) (f (n - c * x) (x + 1)))
          [1 .. n `div` x]

-- | Choose n strings out of a list and join them
-- Used to select subtrees to combine
pick :: Int -> [String] -> [String]
pick _ [] = []
pick 0 _ = [""]
pick n aa@(a:as) = map (a ++) (pick (n - 1) aa) ++ pick n as

-- | Generate all rooted trees with n nodes
-- Builds trees by combining smaller subtrees according to partitions
trees :: Int -> [String]
trees n =
  map (\x -> "(" ++ x ++ ")") $
  concatMap (foldr (prod . build) [""]) (parts (n - 1))
  where
    build (c, x) = pick c $ trees x
    prod aa bb =
      [ a ++ b
      | a <- aa
      , b <- bb ]

-- | Parse command line argument, defaulting to 5
parseArgs :: [String] -> Maybe Int
parseArgs [] = Just 5
parseArgs [arg] = readMaybe arg
parseArgs _ = Nothing

main :: IO ()
main = do
  args <- getArgs
  case parseArgs args of
    Nothing -> do
      hPutStrLn stderr "Usage: list-rooted-trees [n]"
      hPutStrLn stderr "  n: number of nodes (default: 5, must be positive)"
      exitFailure
    Just n
      | n < 1 -> do
          hPutStrLn stderr "Error: n must be positive"
          exitFailure
      | otherwise -> do
          let result = trees n
          mapM_ putStrLn result
          hPutStrLn stderr $ "Number of " ++ show n ++ "-trees: " ++ show (length result)
