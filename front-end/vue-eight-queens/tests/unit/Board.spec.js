import { shallowMount, mount } from '@vue/test-utils'
import Board from '@/components/Board'

describe('Board', () => {

  it('has the same number of rows as props.dimension', () => {
    const testBoard = shallowMount(Board, {
      propsData: {
        dimension: 3
      }
    })
    console.log(`Dimension is ${testBoard.vm.dimension}`)
    const rowCount = testBoard.findAll('.row').length
    console.log(`Row count is ${rowCount}`)
    expect(rowCount).toEqual(testBoard.vm.dimension)

  })

  it('has the same number of columns as props.dimension', () => {
    const testBoard = shallowMount(Board, {
      propsData: {
        dimension: 6
      }
    })
    console.log(`Dimension is ${testBoard.vm.dimension}`)
    const cellCount = testBoard.findAll({name: 'Cell'}).length
    const colCount = cellCount / testBoard.vm.dimension
    console.log(`Column count is ${colCount}`)
    expect(colCount).toEqual(testBoard.vm.dimension)
  })

  it('has the same number of queens as props.queens_count', () => {
    // must use mount here because I need the cell within the board ...
    const testBoard = mount(Board, {
      propsData: {
        dimension: 3,
        queens_count: 3
      }
    })
    const queensCount = testBoard.vm.queens_count
    console.log(`Queens on the board: ${queensCount}`)
    console.log(testBoard.vm.initialState)
    let queenCellArray = testBoard
      .findAll({name: 'Cell'})
      .filter(w => w.vm.$data.hasQueen)
    expect(queenCellArray.length).toEqual(queensCount)
  })
})